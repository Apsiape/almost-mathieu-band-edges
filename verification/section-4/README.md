# Section 4: rational phase-union widths

This sample certifies 23 widths: 19 of 64 original cases and four registered out-of-sample cases. Original parameters: (lambda,p/q)=(3,8/13), A=20,40, D=1,...,5; and (2,13/21), A=10,20,40, D=1,...,3. The new cases use (5,13/21), A=20,40, D=2,3. Extension fractions are (pA+p_previous)/(qA+q_previous). This is a finite rational experiment.

Arb transfer jets at 4096 bits certify extremum brackets and opposite edge signs. Cyclic LDL inertia gives three centre counts equal to D; Chambers' phase-union exclusion extends the count across the parameter torus. Decimal endpoints below round outward. The normalization C_D uses the PARENT derivative, the Sudler product S_(D-1)(q/qprime), and lambda^(q(D-1))/2.

Confirmed rerun environment: Python 3.13.12, NumPy 2.4.3, SciPy 1.17.1, python-flint 0.9.0 (FLINT 3.6.0). All numerical libraries use one thread; each process has a hard 1,200-second timeout.

From the archive root:
~~~text
python -m pip install -r requirements.txt
python -u -B reproduce.py --section 4
python -B validate.py --section 4
~~~
Expected runtime: about 15 seconds. The manifest in inputs/cases.json lists every measurement argument. For an individual case, from this folder:
~~~text
python -u -B code/certify.py measure 5 13 21 20 2 3
~~~
certificates/ preserves original outputs and base-only preregistration; rerun/ holds new outputs. code/analyze.py regenerates slopes and residuals. Widths, predictions, slopes and residuals reproduced exactly.

| A | D | Outward log width | Outward C_D |
|---:|---:|---|---|
| 20 | 2 | [-68.974899318838,-68.974899318837] | [1.023090807413,1.023090807414] |
| 20 | 3 | [-101.720353379131,-101.720353379130] | [1.035248779382,1.035248779383] |
| 40 | 2 | [-67.646792273466,-67.646792273465] | [1.012444999776,1.012444999777] |
| 40 | 3 | [-99.079273854345,-99.079273854344] | [1.018864954559,1.018864954560] |

| lambda | q | D | Outward slope, A=20 to 40 | Target |
|---:|---:|---:|---|---:|
| 2 | 21 | 2 | [1.959062132669,1.959062132670] | 2 |
| 2 | 21 | 3 | [3.895722346085,3.895722346086] | 4 |
| 3 | 13 | 2 | [1.965515948466,1.965515948467] | 2 |
| 3 | 13 | 3 | [3.905399967098,3.905399967099] | 4 |
| 3 | 13 | 4 | [5.793223529481,5.793223529482] | 6 |
| 3 | 13 | 5 | [7.610606702904,7.610606702905] | 8 |
| 5 | 21 | 2 | [1.958796910655,1.958796910656] | 2 |
| 5 | 21 | 3 | [3.895272170999,3.895272171000] | 4 |

The new collapse bands [0.95,1.10] pass. Their slopes pass the unchanged 0.25 tolerances; their corrected-increment residuals are:

- A=20, D=2: [-0.000926402751,-0.000926402750].
- A=40, D=2: [-0.000334532533,-0.000334532532].

Original C_D lies in [1.0045,1.0558]; the smallest original log width is [-71.272126200684,-71.272126200683]. The original universal slope tolerance 0.25 FAILS at D=5. The original corrected residual range is [-0.006598,-0.000488]; the lambda=2,q=21,A=10,D=2 witness is [-0.006597244240,-0.006597244239]. Thus 0.0061 is false; 0.00660 is safe and preserves the 0.02 band. The new residuals pass 0.01.

No q=34 slope was independently reproduced; the source's mixed-pair summary is excluded. No all-64 or irrational-transfer claim follows.
