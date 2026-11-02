# Band edges of the almost Mathieu operator at Liouville scales

Seth Douglas and Nidhal Mghirbi

Version 2.0.1, November 2026. A preprint; it has not been peer reviewed. Version 2.0.0: [10.5281/zenodo.23877075](https://doi.org/10.5281/zenodo.23877075). Version 1.0.0: [10.5281/zenodo.23873797](https://doi.org/10.5281/zenodo.23873797). Concept DOI (all versions): [10.5281/zenodo.23873796](https://doi.org/10.5281/zenodo.23873796).

## Abstract

We study gap decay for the supercritical almost Mathieu operator on both sides of the Liouville threshold. Write L=log(lambda), beta=beta(alpha), x=2 beta/L, and let rho be the liminf of -log|G_m|/(L|m|). For 0<x<1 we prove rho<=1-x. At beta-attaining convergents and every fixed positive integer D, the gap with label -Dq_n sgn(delta_n) has width at least c_D kappa_n^(1-D)/P_n'(E_n), where delta_n=q_n alpha-p_n and kappa_n=(2 pi q_n)^2 lambda^(q_n)|delta_n|^2. The proof keeps the energy-dependent Feshbach self-energy, constructs a common covariant well family with a globally gapped continuation, and resolves the fixed-D avoided crossing by relative tunnelling estimates. Liu-Shi's theorem and IDS-preserving Aubry duality give 1/C<=rho<=1-x<1 for 0<x<=2/C, with an absolute constant C. This contradicts their stated expectation of the sharper upper gap bound in that overlapping range; it does not contradict their theorem. Equality rho=1-x remains open. Above the threshold, our earlier polynomial lower subsequences give rho=0 for finite beta>L/2, and a surplus argument covers beta=infinity. The equality line x=1 remains open. The reductions use rational top-band Green decay, translated Wannier frames and exact finite-box counts. No computation enters a proof.

## Changes in version 2.0.1

- Cites Wencai Liu's doubled Gordon threshold (arXiv:2607.24188). At the completely resonant phases, 2 theta in alpha Z + Z,
  the spectral transition from Anderson localization (Liu, arXiv:2205.04648) to purely singular continuous spectrum lies on the
  same line 2 beta = log(lambda), that is x = 1, as the gap-decay threshold; the introduction and the phase-diagram notes now say
  so. No result changes.

## Changes in version 2.0.0

- New below the Liouville threshold: for 0 < x < 1, with x = 2 beta/log(lambda), the gap-decay rate satisfies rho <= 1 - x.
  At beta-attaining convergents and every fixed positive integer D, the gap with label -D q_n sgn(delta_n) has an explicit
  lower bound on its width.
- With the theorem of Liu and Shi and IDS-preserving Aubry duality this gives 1/C <= rho <= 1 - x < 1 for 0 < x <= 2/C. This
  contradicts Liu and Shi's stated expectation of a sharper upper gap bound in that range; it does not contradict their theorem.
  Equality rho = 1 - x, and the line x = 1, remain open.
- New sections and appendices give the proof: the energy-dependent Feshbach self-energy, a common covariant well family with a
  globally gapped continuation, and relative tunnelling estimates at the fixed-D avoided crossing.
- The Numerical Record gains Sections 4-6, and the new folder verification/ holds the code, inputs and certified outputs of
  the three independent checks they report. The version 1.0.0 results above the threshold are unchanged.

## Contents

The paper is paper/main.pdf (60 pages). Its LaTeX source is paper/main.tex with the section files, paper/figures/ and paper/references.bib; paper/main.bbl is included. Build with pdflatex and BibTeX. No computation is used in any proof.

NUMERICAL-RECORD.md is the accompanying Numerical Record that the paper's certified-check remarks refer to: the registered predictions, their certified comparison intervals (including failed registrations) and, in Sections 4-6, three independent checks of the new results below the threshold. verification/ holds the code, inputs and certified outputs of those three checks (175 files, listed with their SHA-256 sums in verification/SHA256SUMS); verification/README.md says how to rerun them.

## Rights

CC BY 4.0. See RIGHTS.md and LICENSE-CC-BY-4.0.txt.

## Related

- "Exact transport and spectral dimensions for the almost Mathieu operator" (Seth Douglas and Nidhal Mghirbi, 2026), version 2.0.1, [10.5281/zenodo.23864352](https://doi.org/10.5281/zenodo.23864352). It proves the transport law and the spectral dimensions at almost every phase.
- "Universality of the transport law for supercritical quasi-periodic operators" (Seth Douglas and Nidhal Mghirbi, 2026), version 1.0.0, [10.5281/zenodo.23830333](https://doi.org/10.5281/zenodo.23830333). It proves the law at almost every phase for supercritical type I analytic potentials.
- "Worst-case transport and light cones for quasi-periodic operators" (Seth Douglas and Nidhal Mghirbi, 2026), version 2.0.0, [10.5281/zenodo.23875774](https://doi.org/10.5281/zenodo.23875774). It proves the exact worst-case transport law for every finite beta > log(lambda)/2.
