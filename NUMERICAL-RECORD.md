# Numerical Record

Accompanying record for "Band edges of the almost Mathieu operator at Liouville scales" (Seth Douglas and Nidhal Mghirbi),
version 2.0.0, November 2026. The paper's certified-check sections refer to Sections 1-6 below. Sections 1-3 preserve the v1.0.0 record.

This record preserves numerical material that the paper abbreviates: the registered predictions, their certified comparison
intervals, the corrected projector interpretation and the one full-period test that was not computed. Sections 1-3 retain the D77
arithmetic-picture and D80 global-reduction certificates. Sections 4-6 cite the folder verification/ of release v2.0.0 of
https://github.com/Apsiape/almost-mathieu-band-edges (tag v2.0.0), archived on Zenodo under the concept DOI 10.5281/zenodo.23873796.
Those sections specify the independent checks, certified objects, sample sizes and failed registrations. No new numerical campaign
was run to prepare this record. These finite measurements do not prove an irrational asymptotic gap or transport law, and no computation enters any proof in the paper.

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


## 4. Below-threshold rational widths: finite certificates

The new independent gap-width check certified 23 rational phase-union widths: 19 of the 64 submitted cases and four registered out-of-sample cases. Original parents were 8/13 at lambda=3, A=20,40, D=1,...,5, and 13/21 at lambda=2, A=10,20,40, D=1,...,3. No all-64 reproduction is claimed. Arb transfer jets, cyclic LDL inertia, certified extremum brackets and edge signs were used at 4096 bits. The three phase/fibre counts at each gap centre equal D. Chambers' phase-union exclusion then makes the count constant over the parameter torus. These are finite rational certificates, not certificates of irrational transfer.

For the following four out-of-sample cases, lambda=5, parent 13/21, and the extension is (13A+8)/(21A+13). Put omega=21/(21A+13), Lambda=5^21, S_(D-1)(omega)=product_(j=1)^(D-1)|2 sin(pi j omega)|. The normalized constant is C_D=w_D |P_21'(E_D)| S_(D-1)(omega)^2 Lambda^(D-1)/2, with the PARENT polynomial derivative.

| A | D | Outward log-width enclosure | Outward C_D enclosure |
|---:|---:|---|---|
| 20 | 2 | [-68.974899318838,-68.974899318837] | [1.023090807413,1.023090807414] |
| 20 | 3 | [-101.720353379131,-101.720353379130] | [1.035248779382,1.035248779383] |
| 40 | 2 | [-67.646792273466,-67.646792273465] | [1.012444999776,1.012444999777] |
| 40 | 3 | [-99.079273854345,-99.079273854344] | [1.018864954559,1.018864954560] |

All four registered out-of-sample collapse bands [0.95,1.10] pass. The D=2 and D=3 slopes across A=20 to 40 are in [1.958796910655,1.958796910656] and [3.895272170999,3.895272171000], within the unchanged 0.25 tolerances about 2 and 4. Their corrected-increment residuals are [-0.000926402751,-0.000926402750] and [-0.000334532533,-0.000334532532], within the registered 0.01 band.

In the original 19-case sample all normalized constants lie in the outward range [1.0045,1.0558]. The smallest sampled original log width is in [-71.272126200684,-71.272126200683].

| lambda | q | D | Outward slope enclosure across A=20 to 40 | Target |
|---:|---:|---:|---|---:|
| 3 | 13 | 2 | [1.965515948466,1.965515948467] | 2 |
| 3 | 13 | 3 | [3.905399967098,3.905399967099] | 4 |
| 3 | 13 | 4 | [5.793223529481,5.793223529482] | 6 |
| 3 | 13 | 5 | [7.610606702904,7.610606702905] | 8 |
| 2 | 21 | 2 | [1.959062132669,1.959062132670] | 2 |
| 2 | 21 | 3 | [3.895722346085,3.895722346086] | 4 |

The universal original slope band of width 0.25 fails at D=5; it remains a failed registration. A source summary also misclassified a q=34 case by mixing its middle and largest A pairs. No independently reproduced q=34 slope is added here.

For the per-label increment define Delta_D=(log w_D-log w_(D+1))/(Lq), F_D=2 log|2 sin(pi D omega)|/(Lq)+x_n. Compare Delta_D-F_D with 1-x_n. The original-sample residual range is outwardly enclosed by [-0.006598,-0.000488]. At lambda=2,q=21,A=10,D=2 it is [-0.006597244240,-0.006597244239]. Thus the summary's 0.0061 absolute bound is false. The safe original-sample bound 0.00660 preserves the registered 0.02 band. Raw increments without this finite-size correction are not close to the limiting line.

## 5. Complementary Green columns: finite rounded-span certificates

Six of 62 original cases and two independently generated out-of-sample cases were certified. Original exact dyadic input frame coefficients define the finite spans. The out-of-sample frames were constructed independently from 128-node Bloch eigenvectors, rounded to exact dyadics and cut to the specified finite supports; the eigenvector quadrature does not enclose exact infinite-support Wannier functions.

For a box and rounded frame V the solver certifies the bordered equations (E-H)g+V l=delta_0 and V^T g=0, with nonzero tridiagonal pivots and a nonsingular Arb solve for V^T(E-H)^(-1)V. Every residual contains zero; nonsingularity is separately certified. No unresolved tail window is skipped.

The reported Gamma_out is a finite cell-boundary tail rate. On each side of source zero let T(d) be the maximum absolute Green-column value over the entire remaining tail of the finite box at radial distance at least d. The rate at d is (log T(d)-log T(d+2q))/(2q); Gamma_out is the minimum of these rates over all admissible integer d on both sides. The frame-cell edge is max(J)q+floor(q/2) on the right and min(J)q-floor(q/2) on the left. Start at max(q,abs(edge-source)); when J is empty start at q. The SECOND endpoint d+2q must be at least 3q from the box end. Source zero and E-minus are used in every accepted case. The frozen comparison omits every cell containing a frame centre. This exact cell convention supersedes initial wrong-window trials. The original E-minus is its encoded dyadic; the new cases use certified Emax-m0/8. All test energies lie strictly in abs(E-Emax)<m0/4.

| sample | lambda | q | b | Certified Gamma_out | Certified minimum frozen rate |
|---|---:|---:|---:|---|---|
| original 4 | 2 | 21 | .20 | [0.660989590482,0.660989590483] | [0.558111323095,0.558111323096] |
| original 5 | 2 | 34 | .20 | [0.684494173348,0.684494173349] | [0.677341919872,0.677341919873] |
| original 6 | 2 | 13 | .28 | [0.632586166903,0.632586166904] | [0.582432797091,0.582432797092] |
| original 7 | 2 | 21 | .28 | [0.680983561057,0.680983561058] | [0.674495438231,0.674495438232] |
| original 9 | 2 | 13 | .33 | [0.685808798076,0.685808798077] | [0.530028428438,0.530028428439] |
| original 10 | 2 | 21 | .33 | [0.660417326736,0.660417326737] | [0.654977979130,0.654977979131] |
| out of sample 0 | 5 | 21 | .28 | [1.596062732435,1.596062732436] | [1.590786102945,1.590786102946] |
| out of sample 1 | 5 | 21 | .33 | [1.571916026678,1.571916026679] | [1.571268609809,1.571268609810] |

Every original reproduction agrees within its registered .002 tolerance. The new registered rate and frozen-comparison bands pass after disclosed input-rounding and window-protocol corrections; invalid trials remain excluded. These measurements concern finite rounded spans, not the full Schur bound or the rejected isolated infinite-well inverse.

## 6. Continued and physical-box complements: finite rounded-span certificates

The analytic continuation uses one fixed smooth C-infinity clamp. The numerical experiment uses the specified C1 cubic clamp. This distinction is part of the experiment, not a numerical regularity proof.

Let rho_c=(Emax-sup spectrum of H compressed to V-perp)/m0 in each specified Dirichlet matrix. Exact dyadic finite vectors define V. Arb at 512 bits certifies the q-periodic top eigenvalue by the all-eigenvalue Rump solver and computes Pprime from the product of its separations from the other fibre eigenvalues. The direct tridiagonal solves certify S=V^T(E-H)^(-1)V. Constrained inertia is n_minus((E-H)|V-perp)=n_minus(E-H)+n_plus(S)-rank(V). A certified congruence and interval Gershgorin signs certify the inertia of S; every pivot and compressed eigenvalue is separated from zero.

The accepted brackets below have no negative compressed (E-H) eigenvalues at the lower-rho endpoint and a positive number at the upper-rho endpoint. Every case also passes the strict-one test at rho_test=1.000001, so the complement top lies strictly below Emax-m0.

| sample | lambda | q | b | family | Matrix size | rank V | Outward rho_c enclosure |
|---|---:|---:|---:|---|---:|---:|---|
| original 0 | 2 | 13 | .33 | continued | 169 | 1 | [42.512420926115,42.597530877920] |
| original 1 | 2 | 13 | .33 | box | 73 | 1 | [42.512420938688,42.597530890518] |
| original 2 | 2 | 21 | .28 | continued | 490 | 4 | [64.792431937543,64.922146515998] |
| original 3 | 2 | 21 | .28 | box | 358 | 4 | [64.792431937543,64.922146515998] |
| original 4 | 3 | 34 | .25 | continued | 4695 | 27 | [45.396066809179,45.486949825815] |
| original 5 | 3 | 34 | .25 | box | 4915 | 27 | [45.396066809179,45.486949825815] |
| out of sample 0 | 5 | 21 | .28 | continued | 490 | 4 | [66.310252694963,66.323516071840] |
| out of sample 1 | 5 | 21 | .28 | box | 358 | 4 | [66.310252694963,66.323516071840] |
| out of sample 2 | 5 | 21 | .33 | continued | 1088 | 10 | [49.271919945713,49.281775315240] |
| out of sample 3 | 5 | 21 | .33 | box | 1022 | 10 | [49.271919945713,49.281775315240] |

Six of 34 original configurations were independently checked, including both q=34 families. The four new cases use lambda=5, parent 13/21, y=3/10, b=.28,.33, both families. Their exact exponential delta was rounded to binary64 only after an interval check against the adjacent rounding midpoints. Their unchanged prediction bands [60,85] and [45,60] pass. The absolute continued/box differences are certified below .013264 and .009856, hence below the registered .05. Identical printed brackets do not imply identical spectra. Initial coarse certificates were preserved and only the bracket widths were refined.

The frozen-edge normalization constant 9 pi^2/2 is enclosed by [44.41321980490211378475520949944267,44.41321980490211378475520949944269]. For q=34, the ratio of rho_c to (9 pi^2/2)g(t_out)/Mprime is [1.026094870950,1.028149114937]. The new ratios are [1.057070003871,1.057281439016] for b=.28 and [1.037161964181,1.037369417320] for b=.33, within the unchanged [.85,1.15] bands. These are finite-size consistency checks; they do not prove convergence to a constant.

The author's original no-twofold-drop and universal finite-q continued/box agreement predictions failed in preasymptotic examples and remain failures. The new out-of-sample successes do not relabel them.

All new checker campaigns used independent solvers rather than executing submitted solver code. Their accepted measurements were serial, with single-thread numerical libraries and interval arithmetic, external 55-second hard timeouts and a 1.5 GB working-set guard. The recorded maximum working sets were 92,372,992 bytes for the rational-width campaign, 71,495,680 for the Green-column campaign and 72,171,520 for the continuation campaign. No accepted measurement timed out or exceeded its guard. The brief initial import probe in the Green-column check lacked an external kill timer; it was not a measurement. Saved manifests, outward enclosures, invalid-trial exclusions and original registrations remain in the checking archive. No calculation in this record enters a proof.
