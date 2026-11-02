# Verification archive for version 2.0.0

This folder supplies the independent numerical certificates cited by Sections 4-6 of NUMERICAL-RECORD.md in release v2.0.0. Sections 1-3 retain the separate D77/D80 certificates.

| Folder | Numerical Record | Scope |
|---|---|---|
| section-4/ | Section 4 | 23 rational phase-union widths: 19 original and four out of sample |
| section-5/ | Section 5 | Eight complementary Green-column certificates for finite rounded spans |
| section-6/ | Section 6 | Ten finite complement brackets, plus four preserved coarse brackets |

Each README gives methods, exact commands, versions, runtime, results and exclusions. Original certificates and exact inputs are preserved separately from regenerated outputs. CODE-CHANGES.json records source-engine hashes and the portability adaptations. ENVIRONMENT.json and requirements.txt specify the confirmed rerun environment.

From this folder, with Python 3.13.12:
~~~text
python -m pip install -r requirements.txt
python -u -B reproduce.py
python -B validate.py
~~~
Expected total runtime is about 45 seconds. Processes run serially, with one numerical thread and a hard 20-minute limit each. RERUN-RESULTS.json summarizes the confirmed run; per-process timings, commands and logs are in each rerun/ folder. No case exceeded its limit or was skipped. A timeout is recorded as skipped; failed computations stop reproduction.

SHA256SUMS lists every other file, using relative paths and SHA-256. The manifest excludes itself because a file cannot contain its own stable digest. These checks certify finite numerical statements; no computation enters an analytic proof.
