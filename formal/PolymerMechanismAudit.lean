import Mathlib

/-!
Minimal logical certificates for the polymer-electrolyte mechanism audit.

These theorems check implications and countermodels only. They do not validate
any empirical premise, assert that two real samples have exactly equal Tg, or
establish that a real electrolyte obeys `conductivity = carrier * charge *
mobility` without correlation corrections.
-/

namespace ARCClaimClosure.PolymerMechanism

structure ToyMaterial where
  tg : ℚ
  conductivity : ℚ

def materialA : ToyMaterial := { tg := 1, conductivity := 1 }
def materialB : ToyMaterial := { tg := 1, conductivity := 2 }

theorem sameTgDoesNotEntailSameConductivity :
    materialA.tg = materialB.tg ∧
      materialA.conductivity ≠ materialB.conductivity := by
  norm_num [materialA, materialB]

def sigma (carrier charge mobility : ℚ) : ℚ := carrier * charge * mobility

theorem conductivityFactorizationIsNoninjective :
    sigma 1 1 2 = sigma 2 1 1 ∧ (1 : ℚ) ≠ 2 := by
  norm_num [sigma]

/- `axis1Observable` represents `σ * T * τₛ` up to the fixed factor
`q² / k_B`. `carrier` is an effective carrier population, `correlation` is a
collective/Haven factor, and `diffusion * relaxation` is `D * τₛ`. -/
def axis1Observable
    (carrier correlation diffusion relaxation : ℚ) : ℚ :=
  carrier * correlation * diffusion * relaxation

/-- The Wang Axis-1 invariant follows only from the conjunction of constant
carrier population, constant collective correlation, and complete diffusion-
segmental coupling. -/
theorem axis1InvariantUnderCompositeNull
    (p₁ p₂ h₁ h₂ d₁ d₂ τ₁ τ₂ : ℚ)
    (hCarrier : p₁ = p₂)
    (hCorrelation : h₁ = h₂)
    (hCoupling : d₁ * τ₁ = d₂ * τ₂) :
    axis1Observable p₁ h₁ d₁ τ₁ = axis1Observable p₂ h₂ d₂ τ₂ := by
  simp only [axis1Observable]
  rw [hCarrier, hCorrelation]
  calc
    p₂ * h₂ * d₁ * τ₁ = p₂ * h₂ * (d₁ * τ₁) := by ring
    _ = p₂ * h₂ * (d₂ * τ₂) := by rw [hCoupling]
    _ = p₂ * h₂ * d₂ * τ₂ := by ring

/-- A change in the Axis-1 observable refutes the composite null, not any one
premise in isolation. -/
theorem axis1ViolationRefutesCompositeNull
    (p₁ p₂ h₁ h₂ d₁ d₂ τ₁ τ₂ : ℚ)
    (hObserved :
      axis1Observable p₁ h₁ d₁ τ₁ ≠ axis1Observable p₂ h₂ d₂ τ₂) :
    ¬ (p₁ = p₂ ∧ h₁ = h₂ ∧ d₁ * τ₁ = d₂ * τ₂) := by
  rintro ⟨hCarrier, hCorrelation, hCoupling⟩
  exact hObserved
    (axis1InvariantUnderCompositeNull
      p₁ p₂ h₁ h₂ d₁ d₂ τ₁ τ₂ hCarrier hCorrelation hCoupling)

/-- Explicit observation-equivalent countermodel: diffusion remains completely
coupled (`D * τₛ` is unchanged), but a changed carrier population changes
`σ * T * τₛ`. Thus an Axis-1 deviation alone does not prove diffusion-
segmental decoupling. -/
theorem carrierChangeCanMimicAxis1Decoupling :
    ((1 : ℚ) * 1 = (1 / 2 : ℚ) * 2) ∧
      axis1Observable 1 1 1 1 ≠ axis1Observable 2 1 (1 / 2) 2 := by
  norm_num [axis1Observable]

/-- If two distinct mechanisms have the same admitted observation, that
observation cannot uniquely identify the first mechanism. In the Wang audit,
the empirical premise that packing and an alternative mechanism are
observation-equivalent remains external to Lean. -/
theorem observationEquivalentMechanismsRefuteUniqueIdentification
    {Mechanism Observation : Type}
    (predicts : Mechanism → Observation)
    {packing alternative : Mechanism}
    (hDistinct : packing ≠ alternative)
    (hEquivalent : predicts packing = predicts alternative) :
    ¬ ∃! mechanism, predicts mechanism = predicts packing := by
  rintro ⟨witness, _hWitness, hUnique⟩
  have hPacking : packing = witness := hUnique packing rfl
  have hAlternative : alternative = witness :=
    hUnique alternative hEquivalent.symm
  exact hDistinct (hPacking.trans hAlternative.symm)

theorem scopedCounterexampleRefutesUniversalNecessaryImplication
    {α : Type} (P Q : α → Prop) (witness : α)
    (hScope : P witness) (hViolation : ¬ Q witness) :
    ¬ (∀ x, P x → Q x) := by
  intro hUniversal
  exact hViolation (hUniversal witness hScope)

inductive DomainPoint where
  | supportingCase
  | exceptionCase
  deriving DecidableEq

def mechanismPrediction : DomainPoint → Prop
  | .supportingCase => True
  | .exceptionCase => False

theorem localExceptionCanCoexistWithLocalSupport :
    (∃ x, mechanismPrediction x) ∧
      (∃ x, ¬ mechanismPrediction x) := by
  exact ⟨⟨.supportingCase, trivial⟩, ⟨.exceptionCase, by simp [mechanismPrediction]⟩⟩

end ARCClaimClosure.PolymerMechanism
