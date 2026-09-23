#!/usr/bin/env python3
"""Fit the frozen Wang Axis-1 coupled and fractional-coupling models.

Required CSV columns:
  material,T_K,sigma_s_cm,tau_s_s,primary_window

Optional uncertainty columns use natural-log units:
  sigma_log_se,tau_log_se,cov_log_sigma_tau

The script fits log(sigma*T) against log(tau_s), avoiding the shared-variable
regression log(sigma*T*tau_s) versus log(tau_s). It emits predictions and a JSON
summary. It does not assign a microscopic mechanism.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


REQUIRED = {"material", "T_K", "sigma_s_cm", "tau_s_s", "primary_window"}
UNCERTAINTY = {"sigma_log_se", "tau_log_se", "cov_log_sigma_tau"}


def as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def read_rows(path: Path) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED - fields
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        rows = []
        for source_row, row in enumerate(reader, start=2):
            temperature = float(row["T_K"])
            sigma = float(row["sigma_s_cm"])
            tau = float(row["tau_s_s"])
            if not (temperature > 0 and sigma > 0 and tau > 0):
                raise ValueError(f"Non-positive physical input on CSV row {source_row}")
            parsed: dict[str, object] = {
                "source_row": source_row,
                "material": row["material"],
                "T_K": temperature,
                "sigma_s_cm": sigma,
                "tau_s_s": tau,
                "primary_window": as_bool(row["primary_window"]),
                "x": math.log(tau),
                "z": math.log(sigma * temperature),
            }
            for name in UNCERTAINTY:
                parsed[name] = float(row[name]) if name in fields and row[name].strip() else None
            rows.append(parsed)
    return rows


def aicc_from_nll(nll: float, n: int, k: int) -> float:
    aic = 2 * k + 2 * nll
    correction = 2 * k * (k + 1) / (n - k - 1) if n > k + 1 else math.inf
    return aic + correction


def aicc_from_rss(rss: float, n: int, k: int) -> float:
    rss = max(rss, np.finfo(float).tiny)
    base = n * math.log(rss / n) + 2 * k
    correction = 2 * k * (k + 1) / (n - k - 1) if n > k + 1 else math.inf
    return base + correction


def has_complete_uncertainty(rows: list[dict[str, object]]) -> bool:
    return all(
        row["sigma_log_se"] is not None
        and row["tau_log_se"] is not None
        and row["cov_log_sigma_tau"] is not None
        and float(row["sigma_log_se"]) > 0
        and float(row["tau_log_se"]) > 0
        for row in rows
    )


def fit_model(rows: list[dict[str, object]], free_slope: bool) -> dict[str, float | str]:
    x = np.array([float(row["x"]) for row in rows])
    z = np.array([float(row["z"]) for row in rows])
    n = len(rows)
    if n < 3:
        raise ValueError("A fit needs at least three primary-window points")

    uncertainty_mode = has_complete_uncertainty(rows)
    if uncertainty_mode:
        sx = np.array([float(row["tau_log_se"]) for row in rows])
        sz = np.array([float(row["sigma_log_se"]) for row in rows])
        cov = np.array([float(row["cov_log_sigma_tau"]) for row in rows])

        def objective(theta: np.ndarray) -> float:
            alpha = float(theta[0])
            beta = float(theta[1]) if free_slope else -1.0
            variance = sz**2 + beta**2 * sx**2 - 2 * beta * cov
            if np.any(variance <= 0):
                return math.inf
            residual = z - alpha - beta * x
            return float(0.5 * np.sum(residual**2 / variance + np.log(variance)))

        start_beta = float(np.polyfit(x, z, 1)[0]) if free_slope else -1.0
        start_alpha = float(np.mean(z - start_beta * x))
        start = np.array([start_alpha, start_beta]) if free_slope else np.array([start_alpha])
        optimum = minimize(objective, start, method="BFGS")
        if not optimum.success:
            raise RuntimeError(f"EIV optimization failed: {optimum.message}")
        alpha = float(optimum.x[0])
        beta = float(optimum.x[1]) if free_slope else -1.0
        loss = float(optimum.fun)
        aicc = aicc_from_nll(loss, n, 2 if free_slope else 1)
        mode = "errors-in-variables"
    else:
        beta = float(np.polyfit(x, z, 1)[0]) if free_slope else -1.0
        alpha = float(np.mean(z - beta * x))
        residual = z - alpha - beta * x
        rss = float(np.sum(residual**2))
        loss = rss
        aicc = aicc_from_rss(rss, n, 2 if free_slope else 1)
        mode = "unweighted-no-covariance"

    prediction = alpha + beta * x
    return {
        "alpha": alpha,
        "beta": beta,
        "epsilon": 1.0 + beta,
        "loss": loss,
        "aicc": aicc,
        "rmse_log_sigmaT": float(np.sqrt(np.mean((z - prediction) ** 2))),
        "mode": mode,
    }


def loo_rmse(rows: list[dict[str, object]], free_slope: bool) -> float:
    residuals = []
    for index, held_out in enumerate(rows):
        training = rows[:index] + rows[index + 1 :]
        fit = fit_model(training, free_slope)
        prediction = float(fit["alpha"]) + float(fit["beta"]) * float(held_out["x"])
        residuals.append(float(held_out["z"]) - prediction)
    return float(np.sqrt(np.mean(np.square(residuals))))


def analyze(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    by_material: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        if bool(row["primary_window"]):
            by_material.setdefault(str(row["material"]), []).append(row)

    summaries = []
    predictions = []
    for material, group in sorted(by_material.items()):
        group.sort(key=lambda row: float(row["T_K"]))
        if len(group) < 4:
            raise ValueError(
                f"Material {material!r} needs at least four primary-window points "
                "for finite free-model AICc and leave-one-out analysis"
            )
        null = fit_model(group, free_slope=False)
        free = fit_model(group, free_slope=True)
        null_loo = loo_rmse(group, free_slope=False)
        free_loo = loo_rmse(group, free_slope=True)
        delta_aicc = float(null["aicc"]) - float(free["aicc"])
        x_span_decades = (
            max(float(row["x"]) for row in group) - min(float(row["x"]) for row in group)
        ) / math.log(10)
        implied_decades = abs(float(free["epsilon"])) * x_span_decades
        summaries.append(
            {
                "material": material,
                "n_primary": len(group),
                "fit_mode": free["mode"],
                "null_beta": -1.0,
                "free_beta": free["beta"],
                "epsilon": free["epsilon"],
                "tau_span_decades": x_span_decades,
                "implied_sigmaTtau_change_decades": implied_decades,
                "null_aicc": null["aicc"],
                "free_aicc": free["aicc"],
                "delta_aicc_null_minus_free": delta_aicc,
                "null_loo_rmse_log_sigmaT": null_loo,
                "free_loo_rmse_log_sigmaT": free_loo,
                "model_preference_only": (
                    "free-slope" if delta_aicc >= 6 and free_loo < null_loo else "not-resolved"
                ),
                "interpretation_ceiling": (
                    "Tests the composite M0 only; does not identify carrier, correlation, "
                    "hopping, packing, or morphology mechanism."
                ),
            }
        )
        for row in group:
            for model_name, fit in (("M0_coupled", null), ("M1_fractional", free)):
                predicted_z = float(fit["alpha"]) + float(fit["beta"]) * float(row["x"])
                predictions.append(
                    {
                        "source_row": row["source_row"],
                        "material": material,
                        "T_K": row["T_K"],
                        "model": model_name,
                        "observed_sigma_s_cm": row["sigma_s_cm"],
                        "predicted_sigma_s_cm": math.exp(predicted_z) / float(row["T_K"]),
                        "residual_log_sigmaT": float(row["z"]) - predicted_z,
                    }
                )
    if not summaries:
        raise ValueError("No rows marked primary_window=true")
    return summaries, predictions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-predictions", type=Path, required=True)
    args = parser.parse_args()

    rows = read_rows(args.input)
    summaries, predictions = analyze(rows)
    payload = {
        "schema_version": "wang-axis1-model-comparison-0.1",
        "input": str(args.input.resolve()),
        "models": {
            "M0": "log(sigma*T)=alpha-log(tau_s)",
            "M1": "log(sigma*T)=alpha+beta*log(tau_s); epsilon=1+beta",
        },
        "summaries": summaries,
        "scientific_scope": (
            "Model comparison for the composite coupling null. A free-slope preference "
            "does not identify a microscopic mechanism."
        ),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_predictions.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    with args.output_predictions.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
    print(json.dumps(summaries, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
