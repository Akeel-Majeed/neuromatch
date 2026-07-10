# Project Map — Zhong et al. 2025 (80,000-neuron supervised/unsupervised learning)

**Dataset in one line:** 2-photon calcium imaging of ~20k–90k mouse visual-cortex neurons
(V1 + medial/lateral/anterior HVAs), before vs. after learning, across cohorts:
**task** (rewarded) · **unsupervised** (same stimuli, no reward) · **grating** (exposure control) · **naive**.
Responses shipped **PCA-compressed** (raw is huge). Stimuli: leaf/circle/rock/brick textures + gratings.
Paper's core claim: *most* learning plasticity is **unsupervised** (medial HVAs, visual-not-spatial);
the *only* supervised signal is a **reward-prediction ramp in anterior HVAs**. → see `ZHONGETAL_summary.md`.

Tiers:  🟢 green = core, do-after-intro-notebook   🟡 yellow = needs pipeline mods   🔴 red = open-ended theory

```
        CORE CHAIN (Q1-4)                    BRANCHES                        EXTENSIONS
        ================                     ========                        ==========

   ┌──────────────────────┐
   │ Q1 🟢 PCA sanity     │──────────────┐
   │ does PCA space match │              │
   │ raw? can you analyse │              ▼
   │ in it?               │   ┌──────────────────────┐          ┌──────────────────────┐
   └──────────┬───────────┘   │ Q5 🟡 linear-in-PCA  │─────────▶│ Q9 🔴 beyond PCA:    │
              │               │ run analyses in PCA  │          │ ICA/NMF/GPFA — any   │
              ▼               │ space, map back to   │          │ advantage over PCA?  │
   ┌──────────────────────┐   │ neural space         │          └──────────────────────┘
   │ Q2 🟢 position       │   └──────────────────────┘
   │ selectivity /        │
   │ tuning curves        │   ┌──────────────────────┐          ┌──────────────────────┐
   └──────────┬───────────┘   │ Q6 🟡 theory:        │─────────▶│ Q10 🔴 test your     │
              │            ┌─▶│ why is plasticity    │          │ theory (Q6/7/11) in  │
              ▼            │  │ useful? V1 vs higher │          │ THIS data — or design│
   ┌──────────────────────┐│  │ areas differ?        │          │ a new experiment +   │
   │ Q3 🟢 plasticity     ││  └──────────────────────┘          │ null hypothesis      │
   │ FROM learning:       ││                                    └──────────────────────┘
   │ selectivity before   ││  ┌──────────────────────┐                     ▲
   │ vs after task        ││  │ Q7 🟡 predictive     │─────────────────────┤
   └──────────┬───────────┘├─▶│ coding: novelty resp │                     │
              │            │  │ to "leaf2"/"circle2"?│                     │
              ▼            │  └──────────────────────┘                     │
   ┌──────────────────────┐│                                    ┌──────────────────────┐
   │ Q4 🟢 plasticity     ││  ┌──────────────────────┐          │ Q11 🔴 theory:       │
   │ WITHOUT reward:      │└─▶│ Q8 🟡 invariant obj  │─────────▶│ V1→medial→ant→lat    │
   │ analyse unsupervised │   │ recognition: texture │          │ sequential or        │
   │ exploration sessions │   │ neurons firing       │          │ parallel hierarchy?  │
   └──────────────────────┘   │ everywhere in one    │          └──────────────────────┘
                              │ corridor, "learned"? │
                              └──────────────────────┘
```

## What each node actually asks + how you'd attack it

| Q | Question | Simplest method | Rigor trap to watch |
|---|----------|-----------------|---------------------|
| **Q1** 🟢 | Do PCA-compressed responses preserve what raw data shows? | Redo a raw-data plot (a tuning curve) in PCA space, reconstruct, compare | None — this is your warm-up + validity check for everything downstream |
| **Q2** 🟢 | Do neurons have position selectivity in the corridor? Why would visual cortex? | PSTH / tuning curve of response vs. corridor position | Plot single-neuron **and** population; state what "position" means (visual vs spatial) |
| **Q3** 🟢 | What plasticity is driven by *task* learning? | Selectivity (d′) before vs after, **task cohort** | **Train/test split** when selecting "selective" neurons — else circular |
| **Q4** 🟢 | What plasticity arises from *unsupervised* exploration alone? | Same d′ analysis on **unsupervised cohort**; compare to Q3 | The paper's headline lives here. Compare against **grating** cohort to prove stimulus-specificity |
| **Q5** 🟡 | Which linear analyses transfer cleanly through PCA space? | Coding-direction / regression in PCA space, project back | "Advantages" = speed/denoising — quantify, don't assert |
| **Q6** 🟡 | *Theory:* why would V1 vs higher areas need different plasticity? | Argument + a decode-by-region comparison as evidence | It's a hypothesis; make it **falsifiable** and say what data would break it |
| **Q7** 🟡 | Does predictive coding predict novelty responses to leaf2/circle2? | Compare pre/post novelty-response size across regions | Novelty = adaptation over exposure; need before/after **and** a control stimulus |
| **Q8** 🟡 | Are there position-**invariant** texture neurons? Are they "learned"? | Find neurons responsive across a whole corridor; compare cohorts | **Selecting on invariance then "showing" invariance = circular.** Use held-out trials |
| **Q9** 🔴 | Does ICA/NMF/GPFA beat PCA here? | Swap the decomposition, compare reconstruction/decoding | Complex-method trap — only if a simple analysis genuinely stalls |
| **Q10** 🔴 | Can you test a Q6/7/11 theory in this data — or design the experiment? | Predictions + contrasting **null** hypothesis | Where a negative result is a *real* result — design the ideal experiment in detail |
| **Q11** 🔴 | Is the V1/medial/anterior/lateral hierarchy sequential or parallel? | Response-latency / cross-region decoding across areas | Big-idea theory; anchor to what the 4 regions actually let you measure |

## Picking a proposal path (200–300 words, W2D1)

Every proposal needs: a **concrete question**, a **testable hypothesis**, the **cohort comparison** that answers it,
and how you'd **know it worked**. Three ready-made shapes:

- **Safe / green — "Is cortical plasticity supervised or unsupervised?"** → Q1→Q2→Q3→Q4.
  Replicate the paper's core dissociation on the medial region: d′ selectivity rises after learning
  in task **and** unsupervised cohorts but not grating. Answerable with the intro notebook. Lowest risk.
- **Predictive-coding angle — Q3/4 → Q7.** Hypothesis: novelty responses to leaf2/circle2 shrink with
  exposure (a prediction-error signature), reward-independently. Connects to a **big idea** (Part 11: predictive coding).
- **Invariance angle — Q2 → Q8.** Hypothesis: position-invariant texture neurons emerge with learning.
  Highest circularity risk — commit up front to selecting neurons on train trials, testing invariance on held-out trials.

**The three rigor rules that apply to every path:** (1) always **train/test split**, even for tuning curves;
(2) any step that **selects or sorts** neurons on the effect you're about to "find" is circular — add a shuffle/held-out control;
(3) the key comparison is almost always **cohort vs cohort** (task vs unsupervised vs grating), not just before-vs-after.

**Note on Q10:** it's not a standalone project — it's the "test it / design the experiment" cap on any theory branch (Q6, Q7, Q11).
A negative result there is fine and reportable; the deliverable becomes a well-specified hypothetical experiment.

---
*Map of the official Zhong et al. project template. Not your proposal — a menu to choose and narrow one.
Green = start here. Refine the question before reaching for Q9's fancier tools. Check dataset specifics with your Project TA.*
