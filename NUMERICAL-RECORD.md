# Numerical Record

Accompanying record for "Band edges of the almost Mathieu operator at Liouville scales" (Seth Douglas and Nidhal Mghirbi),
version 1.0.0. Section 4.3 of the paper refers to Sections 1-3 below.

This record preserves numerical material that the paper abbreviates: the registered predictions, their certified comparison
intervals, the corrected projector interpretation and the one full-period test that was not computed. Every number comes from
the two independent verification reports that the paper calls D77 (the arithmetic picture, its Section 5 and its out-of-sample
supplement) and D80 (the repaired global reduction, its independent certified arithmetic). No new calculation was made for this
record. These finite measurements do not prove the irrational asymptotic gap or transport laws, and no computation enters any
proof in the paper.

## 1. Translated construction, projector correction and failed predictions

All three cases have parent p/q=5/13. G uses lambda=2, theta=0.0377, hbar=0.1, three wells. H uses the same coupling/phase, hbar=0.005, two wells. OOS was registered before measurement: lambda=3, theta=0.0193, hbar=0.1, three wells. In each case delta=hbar/(2*pi*q*lambda^(q/2)).

| Case | Inclusive box | Counts at D=1,...,6 | Maximum dipole-shifted level-error enclosure, in units 2hbar/P_*′ |
|---|---|---|---|
| G | [731,222520] | 3,6,9,12,15,18 | [0,0.000282844609] |
| H | [14638,2971820] | 2,4,6,8,10,12 | [0,0.000314943324] |
| OOS | [256912,3351000] | 3,6,9,12,15,18 | [0,0.000013630460] |

Each row includes counts at the three interior window fractions and midpoint counts after moving both endpoints by −1000 or +1000 sites.

The ground-cluster projector gives these per-well translated-anchor shares:

- G: [0.9558209196836182962179037231977 ± 1.93e−32].
- OOS: [0.98136338757751036956774744137 ± 3.53e−30].

These are spectral-subspace projector weights. Individual eigenvectors can mix within nearly degenerate clusters. The original single-eigenvector weight registration **failed**; a later, separately identified projector correction **passed**. It is not an original success. The residual-growth prediction also **failed**: residuals decrease with D in G, and H has a larger error than G. For the old fixed class, the outward-safe enclosure is [0,0.002]. Its largest quoted share is about 0.00184243687751723, so the old literal bound 0.0018 was too small; rounding inward does not certify it.

## 2. Gap-switch/TP1 registrations and remaining uncomputed test

TP1 is a defined derivative proxy. It is not a measured transport exponent or a proved exact physical burst threshold.

| Independent comparison | Certified result | Status |
|---|---|---|
| q=13, lambda=2, original factor-30 gap/TP1 criterion | Entire refined crossing/TP1 ratio is strictly between 37.3 and 38.3. | Original registration **failed**. |
| q=21, lambda=2, original factor-30 comparison | Entire refined crossing/TP1 ratio is strictly between 99.1 and 101.3. | Factor-30 registration **failed**. |
| q=21, lambda=2, revised coefficient comparison | Measured coefficient bracket [1.088,1.112] lies within [0.97,1.16]. | This revised finite sample passes; it does not establish a uniform asymptotic law. |
| q=21, lambda=5, literal revised TP1 interval | Registered kappa_T1 range [0.0784193310658,0.0937798185941]; actual [0.0782674171360622753052893 ± 5.53e−27]. | Literal interval **failed**. |

For q=13, lambda=2, the independently certified TP1 value is [0.0376688062486264787236542 ± 4.93e−28]. For q=21, lambda=2, it is [0.0142270521276846992252853 ± 1.95e−26]. The latter original gap crossing is bracketed by kappa in [1.4107885091,1.4407223747], with a safe x bracket [1.6457,1.6473]. These are crossing enclosures, not proofs of uniqueness.

For q=21, lambda=5, the actual coefficient relative to the preregistered fixed constant 1.4261 is [0.968120915980743662004981 ± 1.75e−25], strictly below 0.97. Its x_T1 is [1.36429230840289689131962 ± 5.92e−25]. The number rounds to 0.97 at two decimal places; that does not make a strict interval pass. The unquantified big-O offset hypothesis and a strict finite-interval registration are different assertions.

The full original q=21, lambda=5 gap-switch calculation remains **NOT CERTIFIED**. A finite-section proxy gave the candidate kappa bracket [1.3989875341,1.4485054061], but lacks the full-period/exterior exclusion certificate. Agreement of two finite boxes is not a substitute. No asymptotic complementarity conclusion follows from these checks, and a revised hypothesis does not retroactively pass an earlier failed registration.

## 3. Retained rational Mathieu-collapse certificates

D77 encloses a crossing G1=2G2 in kappa_*=[1.4260784738 ± 6.60e−11]. This is a certified crossing enclosure, not a global uniqueness result.

| Parent | lambda | Next coefficient A | Absolute label | Enclosure of log(w*P′/G_D) |
|---|---:|---:|---:|---|
| 2/3 | 5 | 699 | 3 | [0.0001979253,0.0001979254] |
| 3/5 | 5 | 2000 | 10 | [0.0000162096,0.0000162097] |
| 3/5 | 2 | 600 | 15 | [−0.0005267205,−0.0005267204] |
| 8/13 | 5 | 385 | 78 | [0.0039697174,0.0039697175] |
| 8/13 | 2 | 77 | 52 | [0.0172042988,0.0172042989] |
| 5/8 | 2 | 200 | 16 | [0.0003463309,0.0003463310] |
| 3/5 | 5 | 60 | 15 | [0.0091106244,0.0091106245] |
| 2/3 | 5 | 69 | 3 | [0.0034522615,0.0034522616] |
| 8/13 | 2 | 385 | 13 | [0.0005374229,0.0005374230] |
| 2/3 | 5 | 149 | 6 | [0.0008759784,0.0008759785] |

There are ten cases and eight distinct labels. They test the rational phase-union width prediction conditional on the measured locations. All signs, upper endpoints and the maximum residual are preserved. No computation enters an analytic proof in the paper.
