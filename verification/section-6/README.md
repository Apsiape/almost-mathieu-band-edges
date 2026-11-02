# Section 6: continued and physical-box complements

Six of 34 original configurations and four registered out-of-sample configurations are certified. Exact binary64 frame coefficients define finite spans, truncated to each Dirichlet interval. The experiment uses the specified C1 cubic clamp; the analytic construction uses a fixed C-infinity clamp. The two notions of regularity are distinct.

At 512 bits, Arb's all-eigenvalue Rump solver certifies the q-periodic top eigenvalue and the product formula for Pprime. Tridiagonal solves certify S=V^T(E-H)^(-1)V. Constrained inertia is n_minus(E-H)+n_plus(S)-rank(V). A Gram row-sum bound certifies full rank; interval Gershgorin signs after a certified congruence certify inertia. Every pivot excludes zero. Decimal endpoints round outward.

Confirmed rerun environment: Python 3.13.12, NumPy 2.4.3, SciPy 1.17.1, python-flint 0.9.0 (FLINT 3.6.0). All numerical libraries use one thread; each process has a hard 1,200-second timeout.

From the archive root:
~~~text
python -m pip install -r requirements.txt
python -u -B reproduce.py --section 6
python -B validate.py --section 6
~~~
Expected runtime: about 15 seconds, including all four coarse new brackets. Individual case, from this folder:
~~~text
python -u -B code/certify.py oos 0 --replay-bracket
~~~
The earlier engine is code/certify_coarse.py. It produced the six original and four coarse new certificates. The refined engine narrows only new brackets. inputs/ contains only the parameter/frame files consumed by these cases. Archived exact new frames are used by default; --generate-frame repeats the 128-node builder for the same case. Delta's nearest-binary64 rounding is interval-checked.

The rerun recomputes inertia at the archived decimal endpoints: zero negative compressed eigenvalues at the lower-rho endpoint and a positive count at the upper endpoint. All ten strict-one tests at rho=1.000001 pass. Four coarse new brackets are also recertified. No additional cases are introduced.

| Sample | lambda | q | b | Family | N | Rank | Outward rho_c |
|---|---:|---:|---:|---|---:|---:|---|
| original 0 | 2 | 13 | .33 | cont | 169 | 1 | [42.512420926115,42.597530877920] |
| original 1 | 2 | 13 | .33 | box | 73 | 1 | [42.512420938688,42.597530890518] |
| original 2 | 2 | 21 | .28 | cont | 490 | 4 | [64.792431937543,64.922146515998] |
| original 3 | 2 | 21 | .28 | box | 358 | 4 | [64.792431937543,64.922146515998] |
| original 4 | 3 | 34 | .25 | cont | 4695 | 27 | [45.396066809179,45.486949825815] |
| original 5 | 3 | 34 | .25 | box | 4915 | 27 | [45.396066809179,45.486949825815] |
| out of sample 0 | 5 | 21 | .28 | cont | 490 | 4 | [66.310252694963,66.323516071840] |
| out of sample 1 | 5 | 21 | .28 | box | 358 | 4 | [66.310252694963,66.323516071840] |
| out of sample 2 | 5 | 21 | .33 | cont | 1088 | 10 | [49.271919945713,49.281775315240] |
| out of sample 3 | 5 | 21 | .33 | box | 1022 | 10 | [49.271919945713,49.281775315240] |

New bands [60,85] for b=.28 and [45,60] for b=.33 pass. Absolute continued/box differences are below .013264 and .009856, hence below .05. Identical printed brackets do not assert identical spectra.

The constant 9 pi^2/2 lies in [44.41321980490211378475520949944267,44.41321980490211378475520949944269]. Ratios to (9 pi^2/2)g(t_out)/Mprime are:

| Sample | Outward ratio |
|---|---|
| q=34 original | [1.026094870950,1.028149114937] |
| new b=.28 | [1.057070003871,1.057281439016] |
| new b=.33 | [1.037161964181,1.037369417320] |

New ratios pass [.85,1.15]. Original no-twofold-drop and universal finite-q family-agreement predictions remain failed in preasymptotic examples; reported-failures.json records their status without claiming independent recertification. These finite rounded-span tests do not establish an infinite-volume complement bound or asymptotic convergence.
