# Section 5: complementary Green columns

Six of 62 original cases and two out-of-sample cases are certified. Exact dyadic finite frame coefficients define the spans. New frames came from independently generated 128-node Bloch eigenvectors, rounded to dyadics and cut to finite supports; quadrature does not certify infinite-support Wannier functions.

At 4096 bits, Arb tridiagonal solves and a nonsingular bordered solve certify (E-H)g+V l=delta_0 and V^T g=0. Every residual contains zero; every tridiagonal pivot excludes zero. All energies lie strictly within m0/4 of Emax. Source zero and E-minus are used throughout.

For each side let T(d) maximize |g| over the entire remaining tail at distance at least d. Gamma_out minimizes (log T(d)-log T(d+2q))/(2q) over every admissible integer d. The frame-cell edges are max(J)q+floor(q/2) and min(J)q-floor(q/2). Start at max(q,abs(edge)); an empty J starts at q. The second endpoint stays at least 3q from the box end. Frozen comparison omits all cells containing frame centres. No unresolved window is skipped. Table endpoints round outward.

Confirmed rerun environment: Python 3.13.12, NumPy 2.4.3, SciPy 1.17.1, python-flint 0.9.0 (FLINT 3.6.0). All numerical libraries use one thread; each process has a hard 1,200-second timeout.

From the archive root:
~~~text
python -m pip install -r requirements.txt
python -u -B reproduce.py --section 5
python -B validate.py --section 5
~~~
Expected runtime: about 15 seconds, including two excluded rounding trials. Individual accepted new case, from this folder:
~~~text
python -u -B code/certify.py oos 0 4096
~~~
Original case example:
~~~text
python -u -B code/certify_before_rounding_fix.py original 4 4096
~~~
The preserved earlier engine produced original certificates; its input-rounding defect affects only new-frame generation. Accepted new inputs recheck nearest-binary64 rounding of exp(-bq) and -3 delta/10. Certification defaults to archived exact frames. To repeat the original frame builder for the same case, append --generate-frame.

inputs/ holds only the six selected original entries and two accepted new inputs. certificates/ holds eight accepted outputs. Every scientific JSON field reproduced exactly, excluding timing and adapted-script hashes.

| case | lambda | q | b | certified Gamma_out | certified minimum frozen rate |
|---|---:|---:|---:|---|---|
| original 4 | 2 | 21 | 0.2 | [0.660989590482, 0.660989590483] | [0.558111323095, 0.558111323096] |
| original 5 | 2 | 34 | 0.2 | [0.684494173348, 0.684494173349] | [0.677341919872, 0.677341919873] |
| original 6 | 2 | 13 | 0.28 | [0.632586166903, 0.632586166904] | [0.582432797091, 0.582432797092] |
| original 7 | 2 | 21 | 0.28 | [0.680983561057, 0.680983561058] | [0.674495438231, 0.674495438232] |
| original 9 | 2 | 13 | 0.33 | [0.685808798076, 0.685808798077] | [0.530028428438, 0.530028428439] |
| original 10 | 2 | 21 | 0.33 | [0.660417326736, 0.660417326737] | [0.654977979130, 0.654977979131] |
| out of sample 0 | 5 | 21 | 0.28 | [1.596062732435, 1.596062732436] | [1.590786102945, 1.590786102946] |
| out of sample 1 | 5 | 21 | 0.33 | [1.571916026678, 1.571916026679] | [1.571268609809, 1.571268609810] |

Original reproductions pass the unchanged .002 tolerances. New bands [1.50,1.75], Gamma_out >= log(5)-b/4-.02, and frozen-rate differences <=.06 all pass.

excluded/ preserves centre-window, offset-window and rounding-invalid results, plus the two invalid rounding inputs. These remain excluded. Only the rounding-invalid trials were rerun, using their own frozen inputs and earlier engine; their scientific outputs reproduced exactly. The earlier window trials are historical invalid outputs, not accepted certificates.

These are finite rounded-span and finite-tail measurements. They do not certify the full Schur bound or an isolated infinite-well inverse.
