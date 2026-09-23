import Mathlib

/-!
A bounded arithmetic certificate for the public NASICON kMC initialization.

Two supplied configurations at the same composition and temperature have mean
active-event migration barriers that differ by less than 0.25 meV after
rounding to six decimals, while their aggregate initial hopping rates differ.

This theorem does not equate the aggregate initial rate with conductivity and
does not validate the empirical or kinetic premises of the source model.
-/

namespace ARCClaimClosure.NasiconBarrier

inductive Configuration where
  | structure48
  | structure49
  deriving DecidableEq

def meanBarrierMeV : Configuration → ℚ
  | .structure48 => 317094455 / 1000000
  | .structure49 => 316886302 / 1000000

def aggregateInitialRateInPHz : Configuration → ℚ
  | .structure48 => 3986629 / 1000000
  | .structure49 => 2675730 / 1000000

def barrierToleranceMeV : ℚ := 25 / 100

theorem meanBarriersEquivalentAtDeclaredTolerance :
    |meanBarrierMeV .structure48 - meanBarrierMeV .structure49| ≤
      barrierToleranceMeV := by
  norm_num [meanBarrierMeV, barrierToleranceMeV, abs_of_nonneg]

theorem aggregateInitialRatesDiffer :
    aggregateInitialRateInPHz .structure48 ≠
      aggregateInitialRateInPHz .structure49 := by
  norm_num [aggregateInitialRateInPHz]

theorem meanBarrierDoesNotIdentifyAggregateInitialRate :
    |meanBarrierMeV .structure48 - meanBarrierMeV .structure49| ≤
        barrierToleranceMeV ∧
      aggregateInitialRateInPHz .structure48 ≠
        aggregateInitialRateInPHz .structure49 := by
  exact ⟨meanBarriersEquivalentAtDeclaredTolerance, aggregateInitialRatesDiffer⟩

end ARCClaimClosure.NasiconBarrier
