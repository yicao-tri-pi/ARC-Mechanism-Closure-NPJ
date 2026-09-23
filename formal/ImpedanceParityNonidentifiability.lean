import Mathlib

/-!
An algebraic certificate for the measurement complementarity of linear EIS and
second-harmonic NLEIS in a two-electrode model.

The linear full-cell observable is represented as the sum of positive- and
negative-electrode contributions. A compensating shift between those latent
contributions preserves that sum. The opposite-parity second-harmonic
observable is represented as their difference and changes under the same
shift. Thus linear EIS alone does not identify the electrode allocation in
this declared model class, while a second-harmonic measurement can separate
the witness pair.

This theorem validates only the algebra. It does not establish that a physical
cell obeys the model or that experimental noise permits practical separation.
-/

namespace ARCClaimClosure.ImpedanceParity

def linearEIS (positive negative : ℚ) : ℚ := positive + negative

def secondHarmonicNLEIS (positive negative : ℚ) : ℚ := positive - negative

theorem compensatingShiftPreservesLinearEIS
    (positive negative shift : ℚ) :
    linearEIS (positive + shift) (negative - shift) =
      linearEIS positive negative := by
  simp [linearEIS]

theorem nonzeroShiftChangesSecondHarmonic
    (positive negative shift : ℚ) (hShift : shift ≠ 0) :
    secondHarmonicNLEIS (positive + shift) (negative - shift) ≠
      secondHarmonicNLEIS positive negative := by
  simp [secondHarmonicNLEIS]
  intro h
  have : 2 * shift = 0 := by linarith
  exact hShift (by linarith)

theorem linearEISDoesNotIdentifyElectrodeAllocation :
    linearEIS 3 1 = linearEIS 2 2 ∧
      secondHarmonicNLEIS 3 1 ≠ secondHarmonicNLEIS 2 2 := by
  norm_num [linearEIS, secondHarmonicNLEIS]

end ARCClaimClosure.ImpedanceParity
