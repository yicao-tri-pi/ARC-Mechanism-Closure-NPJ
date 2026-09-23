from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite
import re
from typing import Mapping

import sympy as sp

from .schema import Countermodel


_ALLOWED_FUNCTIONS = {"exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt, "Abs": sp.Abs}
_IDENTIFIER = re.compile(r"[A-Za-z_]\w*")
_SAFE_CHARACTERS = re.compile(r"^[A-Za-z0-9_+\-*/()., \t]+$")


@dataclass(frozen=True)
class CountermodelResult:
    valid: bool
    observable_a: float
    observable_b: float
    target_a: float
    target_b: float
    reason: str


def _evaluate(expression: str, values: Mapping[str, float]) -> float:
    if "__" in expression or not _SAFE_CHARACTERS.fullmatch(expression):
        raise ValueError("expression contains unsupported syntax")
    identifiers = set(_IDENTIFIER.findall(expression))
    unknown = identifiers - set(values) - set(_ALLOWED_FUNCTIONS)
    if unknown:
        raise ValueError(f"expression contains undeclared identifiers: {sorted(unknown)}")
    symbols = {name: sp.Symbol(name, real=True) for name in values}
    parsed = sp.sympify(expression, locals={**symbols, **_ALLOWED_FUNCTIONS})
    result = float(sp.N(parsed.subs({symbols[k]: v for k, v in values.items()})))
    if not isfinite(result):
        raise ValueError("expression did not evaluate to a finite scalar")
    return result


def verify_countermodel(countermodel: Countermodel) -> CountermodelResult:
    """Verify same observables but a different scientific target.

    This is deliberately a bounded certificate: it verifies the supplied witness pair
    inside the declared symbolic model class. It does not establish that the model class
    exhausts nature.
    """

    try:
        observable_a = _evaluate(countermodel.observable_expression, countermodel.witness_a)
        observable_b = _evaluate(countermodel.observable_expression, countermodel.witness_b)
        target_a = _evaluate(countermodel.target_expression, countermodel.witness_a)
        target_b = _evaluate(countermodel.target_expression, countermodel.witness_b)
    except (ArithmeticError, TypeError, ValueError, sp.SympifyError) as exc:
        return CountermodelResult(False, float("nan"), float("nan"), float("nan"), float("nan"), str(exc))

    same_observable = isclose(
        observable_a,
        observable_b,
        rel_tol=(
            countermodel.observable_rtol
            if countermodel.observable_rtol is not None
            else countermodel.atol
        ),
        abs_tol=(
            countermodel.observable_atol
            if countermodel.observable_atol is not None
            else countermodel.atol
        ),
    )
    different_target = not isclose(
        target_a,
        target_b,
        rel_tol=(
            countermodel.target_rtol
            if countermodel.target_rtol is not None
            else countermodel.atol
        ),
        abs_tol=(
            countermodel.target_atol
            if countermodel.target_atol is not None
            else countermodel.atol
        ),
    )
    valid = same_observable and different_target
    reason = (
        "same observable and different target"
        if valid
        else f"same_observable={same_observable}, different_target={different_target}"
    )
    return CountermodelResult(valid, observable_a, observable_b, target_a, target_b, reason)
