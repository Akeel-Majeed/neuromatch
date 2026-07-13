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

## Recent SOTA (>2024) — not cited by Zhong et al.

These postdate or run parallel to the paper and are what a 2026 lit review should
cite as current state of the art. Grouped by which Zhong finding they advance.

| Paper | Venue / year | Link | Advances | Why it's SOTA-relevant |
|-------|--------------|------|----------|------------------------|
| **Nejad, Richards et al. 2025** — "Self-supervised predictive learning accounts for cortical layer-specific representations" | *Nat. Commun.* 16, s41467-025-61399-5 | https://www.nature.com/articles/s41467-025-61399-5 | Self-supervised model (Ref 19 pillar) + predictive coding | Direct successor to Bakhtiari 2021 (Ref 19). Adds L2/3-vs-L5 layer specialization and generates mismatch/error signals matching awake mice — links the "pretraining" model to the novelty/predictive-coding data. Strongest single update. |
| **Heilbron et al. 2026** — "Higher-level spatial prediction in natural vision across mouse visual cortex" | *PNAS* | https://pmc.ncbi.nlm.nih.gov/articles/PMC12829946/ | Predictive coding / novelty (Refs 15, 38 pillar) | Deep generative model of spatial predictability: predictable patches → weaker responses; sensitivity driven by *high-level* structure and long-term world knowledge, not recent experience. Most current predictive-coding-in-mouse-V1 result. |
| **Najafi et al. 2025** — "Unexpected events trigger task-independent signaling in visual cortex" | *iScience* | https://www.sciencedirect.com/science/article/pii/S2589004224029559 | Predictive coding + unsupervised framing | Novelty signaling is *task-independent* — directly echoes Zhong's "plasticity is unsupervised, not reward-driven" claim on the novelty side. |
| **Failor, Carandini & Harris 2025** — "Visual experience orthogonalizes visual cortical stimulus responses" | *Cell Rep.* 44, 115235 (PMID 39888718) | https://www.sciencedirect.com/science/article/pii/S2211124725000063 | Orthogonalization / geometry | Already Ref 35 in your Top 5 — flagged here as the current geometry SOTA (16 citations, mouse V1, sparsening + orthogonalization). |
| **Corbo et al. 2025** — "Discretized representations in V1 predict suboptimal perceptual discrimination" | *Nat. Commun.* 16, s41467-024-55409-1 | https://www.nature.com/articles/s41467-024-55409-1 | Population geometry of perceptual learning | Complements Failor: V1 forms *categorical/discretized* codes near threshold. Alternative geometric story for learning-shaped codes. |
| **Matteucci, Zoccolan et al. 2024** — "Unsupervised learning of mid-level visual representations" (review) | *Curr. Opin. Neurobiol.* | https://iris.sissa.it/retrieve/6bcef871-6f84-482b-859b-6859ee629aef/1-s2.0-S0959438823001599-main.pdf | Overarching unsupervised-representation theme | Review to situate the whole "unsupervised experience shapes representations" thesis — good for the intro/keywords. |

**Optional / theory:** *Contrastive Self-Supervised Learning as Neural Manifold Packing* (NeurIPS 2025) — https://neurips.cc/virtual/2025/poster/116916 — ties contrastive SSL objectives to neural-manifold geometry; only if the group wants a theory pillar.

**Verification note:** Nejad and Heilbron summaries confirmed from the article pages;
Najafi, Corbo, and Matteucci are from search abstracts only — skim before committing.

## How these map onto the paper's findings

- **Unsupervised plasticity is real & visual (not reward-driven):** Refs 20, 21
- **Learning-induced changes in V1 tuning/selectivity:** Refs 10, 35
- **Population geometry / orthogonalization:** Ref 35
- **Novelty responses in V1 & lateral HVAs (predictive coding):** Refs 15, 38
- **Self-supervised "pretraining" as a computational model:** Ref 19
