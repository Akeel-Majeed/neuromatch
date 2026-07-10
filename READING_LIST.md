# Literature Review — Priority Reading List

Top papers for situating our project on **Zhong et al. 2025** (*Nature*,
[doi:10.1038/s41586-025-09180-y](https://doi.org/10.1038/s41586-025-09180-y)) —
unsupervised pretraining and learning-driven plasticity in mouse visual cortex.

Reference numbers below match the citation numbers in the Zhong et al. paper.

## Top 5 (read these first)

| # | Ref | Paper | Why it matters |
|---|-----|-------|----------------|
| 1 | 20 | **Li & DiCarlo 2008**, *Science* 321, 1502–1507 — "Unsupervised natural experience rapidly alters invariant object representation in visual cortex" | The most direct empirical precedent for the headline claim: reward-free visual experience reshapes cortical representations. Read **Ref 21** (Li & DiCarlo 2012, *J. Neurosci.* 32, 6611–6620) alongside for the reward-independence point. |
| 2 | 10 | **Poort et al. 2015**, *Neuron* 86, 1478–1490 — "Learning enhances sensory and multiple non-sensory representations in primary visual cortex" | Closest methodological analog — mouse V1, 2-photon imaging, learning-induced plasticity. Very readable. |
| 3 | 35 | **Failor, Carandini & Harris 2025**, *Cell Rep.* 44, 115235 — "Visual experience orthogonalizes visual cortical stimulus responses via population code transformation" | Anchors Zhong's orthogonalization result; same Carandini/Harris lineage, mouse. |
| 4 | 15 | **Rao & Ballard 1999**, *Nat. Neurosci.* 2, 79–87 — "Predictive coding in the visual cortex" | The predictive-coding anchor for the novelty finding (V1 & lateral HVAs). An NMA "big idea." |
| 5 | 19 | **Bakhtiari, Mineault, Lillicrap, Pack & Richards 2021**, *NeurIPS* 34, 25164–25178 — "The functional specialization of visual cortex emerges from training parallel pathways with self-supervised predictive learning" | The self-supervised-predictive-learning ANN analogy underpinning both "pretraining" and HVA functional specialization. |

## Runners-up

- **Ref 38 — Homann et al. 2022**, *PNAS* 119, e2108882119 — "Novel stimuli evoke excess activity in the mouse primary visual cortex." The direct *empirical* mouse-V1 analog for the novelty finding. Swap in for Ref 15 if the group leans empirical over theory (trades the predictive-coding *concept* for the *data*).
- **Ref 14 — Olshausen & Field 1996**, *Nature* 381, 607–609 — sparse coding. Foundational efficient-coding theory, but least tied to any specific Zhong result. Keep as backup if you want the classical-theory pillar explicit.

## How these map onto the paper's findings

- **Unsupervised plasticity is real & visual (not reward-driven):** Refs 20, 21
- **Learning-induced changes in V1 tuning/selectivity:** Refs 10, 35
- **Population geometry / orthogonalization:** Ref 35
- **Novelty responses in V1 & lateral HVAs (predictive coding):** Refs 15, 38
- **Self-supervised "pretraining" as a computational model:** Ref 19
