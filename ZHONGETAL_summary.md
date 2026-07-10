# Paper Summary: `Unsupervised pretraining in biological neural networks`

> Reference note for the Neuromatch Academy "Supervised and unsupervised learning (Zhong et al., 2025)" neurons-pod dataset. This is the paper behind that dataset. All page/figure references point to the original PDF (`ZHONGETAL.pdf`, 25 pages, Nature reprint). Where a claim is the authors' own, it is marked "The authors state…"; inferences and critiques are marked as such.

---

## 1. Citation and Metadata

* **Title:** Unsupervised pretraining in biological neural networks
* **Authors:** Lin Zhong, Scott Baptista, Rachel Gattoni, Jon Arnold, Daniel Flickinger, Carsen Stringer, Marius Pachitariu. Corresponding authors (per the paper's correspondence statement): Lin Zhong and Marius Pachitariu; Stringer is also marked corresponding (✉) in the byline.
* **Affiliation:** HHMI Janelia Research Campus, Ashburn, VA, USA
* **Year:** 2025 (received 26 Feb 2024; accepted 20 May 2025; published online 18 June 2025)
* **Venue:** *Nature*, Vol. 644, 21 August 2025, pp. 741–748 (Article). Open access (CC BY 4.0).
* **DOI:** https://doi.org/10.1038/s41586-025-09180-y
* **Data:** https://doi.org/10.25378/janelia.28811129.v1 (Janelia)
* **Code:** https://github.com/MouseLand/zhong-et-al-2025
* **Research field:** Systems / computational neuroscience; visual cortical plasticity; perceptual learning; representation learning.
* **Main methods used:** Large-scale two-photon calcium imaging (mesoscope, up to ~90,000 neurons), virtual-reality behavior in head-fixed mice, Suite2p processing, selectivity index (d′), population "coding direction" / similarity index, Rastermap, a reward-prediction index (d′late vs early) with train/test–split neuron selection, retinotopic mapping via a convolutional encoding model, behavioral pretraining experiments.
* **One-sentence summary:** By recording tens of thousands of visual-cortical neurons in mice that either learned a visual task or were merely exposed to the same stimuli without reward, the authors show that most learning-related neural plasticity is *unsupervised* (driven by visual experience, not reward), localizes to medial higher visual areas, follows visual rather than spatial rules, and functionally accelerates later task learning — while a distinct reward-prediction signal in anterior areas is the one clearly *supervised* component.

---

## 2. Executive Summary

Neurons in sensory cortex change their responses as animals learn, and this plasticity is usually assumed to be driven by the task — i.e., by reward and feedback (supervised learning). This paper asks a cleaner question: **is that plasticity actually caused by the task, or would it happen anyway just from seeing the stimuli?** The authors recorded huge neural populations (20,547–89,577 neurons per session) from primary visual cortex (V1) and higher visual areas (HVAs) in mice, using a two-photon mesoscope, before and after learning. They compared a **task cohort** (mice rewarded for discriminating two virtual-reality corridors) against an **unsupervised cohort** (mice that ran through the identical corridors but got no reward and were not water-restricted), plus control cohorts exposed only to gratings, and fully naive mice.

The headline result: **almost all of the learning-related neural changes seen in task mice also appeared in the unsupervised mice.** The changes were strongest in the **medial HVAs**, obeyed **visual rather than spatial** rules (new stimuli that shared visual features but not spatial layout were treated like the trained stimuli), and included an **orthogonalization** of representations as fine discriminations were learned. The one clear exception was a **ramping reward-prediction signal in anterior HVAs**, present *only* in task mice, suppressed by reward delivery, and predictive of the animal's trial-by-trial licking — a plausible substrate for the supervised/reinforcement component. Finally, the authors made and confirmed a prediction: mice given 10 days of **unsupervised pretraining** on the naturalistic corridors subsequently **learned the rewarded task faster** than mice with no pretraining or with grating pretraining. This matters because it reframes a large body of "perceptual learning" literature: much of the neural signature attributed to task learning may in fact be experience-driven unsupervised learning, mirroring how unsupervised pretraining helps artificial neural networks.

---

## 3. Wider Research Context

**Field.** This sits at the intersection of systems neuroscience (mouse visual cortex, two-photon imaging), perceptual learning, and machine-learning theories of representation learning (supervised vs. unsupervised/self-supervised).

**The prior debate.** Decades of work show sensory cortical neurons change their tuning with learning — becoming more selective, more discriminative, or more responsive to trained stimuli (refs 1–13 in the paper: e.g., Schoups et al. 2001 in V1; Poort et al. 2015; Yang & Maunsell 2004 in V4). These changes correlate with behavioral improvement and have therefore been *interpreted* as the neural basis of perceptual learning driven by the task. But correlation with performance does not establish that the *task itself* (reward/feedback) caused the change.

**The competing idea.** Theoretical frameworks have long proposed the brain learns from raw sensory statistics without labels — sparse coding (Olshausen & Field 1996, ref 14), predictive coding (Rao & Ballard 1999, ref 15), the wake–sleep algorithm (Hinton et al. 1995, ref 16), slow feature analysis (Wiskott & Sejnowski 2002, ref 17), free-energy (Friston et al. 2006, ref 18), and modern self-supervised deep learning (refs 19, 48–51: BYOL, BERT, GPT-3, DINO). Experimental support was indirect: reward-independent tuning changes in primate inferotemporal cortex (Li & DiCarlo 2008/2012, refs 20–21), critical-period effects (Blakemore & Cooper 1970, ref 22), and predictive-coding-like anticipatory signals in mouse V1 (Fiser et al. 2016; Furutachi et al. 2024, refs 23–24).

**Why this paper was needed.** No prior study had directly, at scale, *dissociated* supervised from unsupervised contributions to cortical plasticity by holding stimulus experience constant while removing reward. The mesoscope's ability to image up to ~90,000 neurons across many visual areas simultaneously makes this dissociation tractable region-by-region.

**How it fits / what it challenges.** It **challenges the default supervised interpretation** of perceptual-learning plasticity in visual cortex, **extends** the unsupervised-learning tradition by giving it direct large-scale evidence, and **connects** biological plasticity to the deep-learning practice of unsupervised pretraining. It partly reconciles conflicting V1 literature (some studies find more selective neurons after learning, refs 10, 13; others, including this one, do not, refs 34, 35).

---

## 4. Research Question

**Main research question:**
`Is the neural plasticity observed in visual cortex during perceptual/task learning caused by supervised learning (reward and task feedback), or is it in fact unsupervised learning driven simply by exposure to the visual stimuli?`

Sub-questions the paper pursues:
* Where in the visual cortex (V1 vs. medial/lateral/anterior HVAs) does each type of plasticity occur?
* Do the learned representations follow **visual** rules (stimulus features) or **spatial** rules (position/navigation in the corridor)?
* Is there *any* uniquely supervised signal, and if so where and what is it?
* Does unsupervised experience have a **behavioral function** — does it speed up later task learning?

**Why it matters / gap addressed.** A large literature interprets cortical tuning changes as task-driven. If they are largely experience-driven, the interpretation of perceptual learning, the design of learning experiments, and the mapping between brains and self-supervised AI all shift.

**Type of question.** Primarily **causal/mechanistic** (does removing reward remove the plasticity?) combined with **descriptive** (anatomical localization; visual vs. spatial coding) and one **predictive/causal behavioral test** (pretraining → faster learning).

---

## 5. Hypothesis or Aim

The paper is framed around competing hypotheses rather than one confirmatory hypothesis. Explicit hypotheses stated by the authors:

* **Primary (supervised vs. unsupervised):** If plasticity is supervised, it should require reward and appear in task mice but not in unsupervised mice; if unsupervised, it should appear in both. *The authors expected — and found — that most plasticity appears in both* (i.e., is unsupervised).
* **Visual vs. spatial plasticity hypothesis (Fig. 2):** Spatial hypothesis → neurons fire in the same *sequence* for new same-category stimuli in matched positions; visual hypothesis → the statistics of visual features ("leafiness") are learned regardless of position. They expected and found support for the **visual** hypothesis.
* **Orthogonalization hypothesis (Fig. 3):** Fine behavioral discrimination between two similar stimuli (leaf1 vs. leaf2) requires their neural representations to become **orthogonal** (less overlapping). Confirmed in both cohorts.
* **Recognition-memory hypothesis (Fig. 4/Extended Data 6–7):** A more detailed, exemplar-specific representation of the trained stimulus emerges to support recognition memory; tested with new exemplars (leaf3) and spatially swapped corridors.
* **Reward-prediction hypothesis (Fig. 4):** A uniquely supervised signal exists — a reward-prediction/expectation signal — and should appear only in task mice. Found in **anterior HVAs**.
* **Functional prediction (Fig. 5):** Unsupervised plasticity should have a benefit: **unsupervised pretraining accelerates subsequent supervised task learning** (analogy to ANN pretraining). Confirmed behaviorally.

---

## 6. Study Design Overview

* **Type:** Experimental, in vivo, longitudinal (before vs. after learning in the same animals), combining large-scale electrophysiology-scale *optical* recording with behavior, plus a separate behavior-only causal experiment.
* **Design logic:** A **cohort-comparison / natural-manipulation** design. The key manipulation is the **presence vs. absence of reward** while stimulus exposure is held (approximately) constant. Cross-cohort comparisons (task vs. unsupervised vs. unsupervised-grating vs. naive) isolate the supervised component.
* **Recording modality:** Two-photon calcium imaging with a custom large-field-of-view **mesoscope** (Sofroniew et al. 2016, ref 31), GCaMP6s in excitatory neurons, cellular resolution, temporal multiplexing to roughly double neuron count.
* **Behavioral paradigm:** Head-fixed mice on an air-floating ball running through **closed-loop virtual-reality linear corridors** (270° visual field, three LED screens).
* **Independent variables:** reward/no-reward (cohort); stimulus type (naturalistic textures vs. gratings; familiar vs. novel exemplars vs. spatially swapped); learning stage (before/after); brain region (V1, medial, lateral, anterior).
* **Dependent variables:** neural selectivity (d′), spatial-sequence correlations, coding-direction projections and similarity index, reward-prediction index (d′late vs early), and behavioral licking / learning speed.
* **Two experimental arms:**
  1. **Imaging arm** (Figs. 1–4): neural plasticity across cohorts.
  2. **Behavior-only arm** (Fig. 5): a *prospective, randomized* test that unsupervised pretraining accelerates learning — this is the arm that best supports a causal/functional claim.

---

## 7. Participants, Subjects, Data, or Model System

**Animals (imaging arm):**
* 89 recordings in **19 mice** expressing GCaMP6s in excitatory neurons (TetO-GCaMP6s × camK2a-tTa; JAX 024742 × 003010). 13 male, 6 female, 2–11 months old, reverse light cycle.
* Two mice were dark-reared; the authors saw no difference and pooled them (a minor caveat the reader should note).
* 4-mm cranial window over V1, positioned lateral/caudal.
* Per-session neuron counts: **20,547 to 89,577 neurons** (the abstract's "up to 90,000").

**Animals (behavior-only arm, Fig. 5):**
* **23 C57 female mice**, headbar only (no window). Randomly assigned to three pretraining cohorts.

**Cohort/session sample sizes (as reported in figures — note they vary by analysis):**
* Task (imaging): n = 4–5 mice depending on figure.
* Unsupervised (imaging): n = 6–9 mice depending on figure.
* Unsupervised-grating: n = 3 mice (5–6 sessions).
* Naive: n = 7–9 mice (up to 11 sessions).
* Behavior-only: VRn-pretrained n = 11, VRg-pretrained n = 7, no-pretraining n = 5.

**Brain system:** Mouse visual cortex — V1 plus HVAs grouped into four **regions**: **V1**; **medial** (PM posteromedial, AM anteromedial, MMA mediomedialanterior, plus lateral retrosplenial); **lateral** (e.g., LM, AL); **anterior** (e.g., RL, RLL). Region borders were defined by retinotopic mapping and aligned to a reference atlas (Zhuang et al. 2017, ref 33).

**Stimuli:** "Frozen" crops from four large naturalistic texture photographs — **leaf, circle, rock, brick** — spatial-frequency matched between categories to force use of higher-order visual features; plus **gratings** (0°, 45°) as an exposure control. Each mouse used one pair (e.g., leaf–circle). Test exemplars: leaf2/circle2 (new crops), leaf3 (new leaf exemplar), and spatially **swapped** leaf1 corridors.

**Preprocessing:** Suite2p (motion correction, ROI/cell detection, neuropil correction, non-negative spike deconvolution, decay timescale 0.75 s). **All analyses used deconvolved fluorescence traces.** Only running timepoints were analyzed, which also removes reward-consumption stops. (The Methods restrict analysis to running periods but do not state an exact cm/s cutoff in the main text.)

**Sample limitations to flag (inference):** small numbers of imaging mice per cohort (n = 3–9), sex imbalance, pooling of dark-reared animals, and reliance on calcium-imaging-derived "spikes" rather than true electrophysiology.

---

## 8. Experimental Groups, Treatment Groups, and Controls

There is no drug/lesion; the "treatment" is **reward availability and training**. Groups:

| Group | What it is | Why included / comparison |
|---|---|---|
| **Task (supervised) cohort** | VR corridors + water reward for licking in rewarded corridor after a sound cue | The classic "learning" condition; establishes the plasticity to be explained |
| **Unsupervised cohort** | Identical corridors/stimuli, **no reward, not water-restricted** | Key comparison: removes supervision while keeping visual exposure → isolates unsupervised plasticity |
| **Unsupervised-grating cohort** | Exposed to VR corridors with **gratings**, tested on naturalistic stimuli before/after | Controls for the effect of *simply being in VR / general exposure* independent of the specific naturalistic image statistics |
| **Naive mice** | Never trained/exposed to the relevant stimuli | Baseline "before-learning" reference for cross-sectional comparisons |
| **Behavior-only: VRn pretraining** | 10 days unrewarded running through **naturalistic** corridors, then 5 days task | Tests functional benefit of unsupervised naturalistic experience |
| **Behavior-only: VRg pretraining** | 10 days unrewarded **grating** corridors, then 5 days task | Controls whether *any* VR pretraining helps vs. specifically the task-relevant stimuli |
| **Behavior-only: no pretraining** | Straight into 5-day task | Baseline learning speed |

**What each comparison buys:**
* Task vs. unsupervised → is plasticity supervised or unsupervised? (Most is unsupervised.)
* Unsupervised vs. unsupervised-grating → is it driven by the specific naturalistic statistics, not just VR exposure? (Grating exposure did *not* reproduce the plasticity → yes, stimulus-specific.)
* Task/unsupervised vs. naive → before/after learning cross-sectional check.
* Reward-prediction signal: task vs. unsupervised → confirms it is uniquely supervised (absent without reward).

**Causal support.** The imaging arm is a **quasi-experimental cohort comparison** — strong for dissociating reward's contribution, but stimulus exposure between cohorts is only *approximately* matched (task mice additionally learn water/cue/position associations and stop to drink; the authors excluded those timepoints). The **behavior-only pretraining arm (Fig. 5) is a genuine randomized prospective experiment**, and it is what best licenses the causal "pretraining accelerates learning" claim.

---

## 9. Methods and Procedure

**Behavioral protocol.**
* Handling → head-fix acclimation on ball (≥3 days) → running training (≥5 days) → closed-loop VR corridors.
* Corridors presented in pseudo-random order, with a grey inter-corridor space; the textured region spans 0–4 m (the window used for all d′/coding analyses). The VR advances at a fixed 60 cm/s while the mouse runs above a motion-triggering speed threshold (running detected optically; VR stationary otherwise), so all mice get comparable visual experience.
* A **sound cue** at a random position (0.5–3.5 m) marks reward availability in the rewarded corridor. Reward = 2.5 µl water on correct lick (active mode) or passive delivery with 1–1.5 s delay in some imaging mice. **Anticipatory licking** (licks before the cue) is the read-out of learning.
* Training timeline (Fig. 1b): acclimation → Train 1 (discrimination, ~2 wk) → Test 1 (new stimuli leaf2/circle2) → Train 2 (fine discrimination leaf1 vs leaf2) → Test 2 (leaf3) → Test 3 (leaf1 swaps).
* Behavior-only arm simplified: sound cue removed; deterministic reward in a "reward zone" (random start 2–3 m); day 0 passive rewards; 4 days active. Each mouse trained on its own texture pair; VRn mice pretrained on the *same* pair.

**Imaging.** Custom two-photon mesoscope (ref 31), ScanImage acquisition, online z-correction, temporal multiplexing. Suite2p pipeline; deconvolved traces; 0.75 s decay.

**Core analyses (intuitive → technical):**

1. **Selectivity index d′ (Fig. 1f):** how differently a neuron responds in the two corridors, computed over the 0–4 m texture region on running timepoints only. "Selective" = |d′| ≥ 0.3. 2D density maps across cortex made by histogramming selective-neuron positions, Gaussian-smoothing, normalizing by total neurons, aligning to atlas.
   *Formula note:* the paper's Methods write the denominator as the **average of the two standard deviations**, `d′ = (μ₁ − μ₂) / ((σ₁ + σ₂)/2)`, not the RMS pooled-SD form `√((σ₁²+σ₂²)/2)` used in classic signal-detection d′. (The same average-SD denominator is used for the reward-prediction index d′late vs early.) This is a minor, self-consistent definitional choice; the |d′| ≥ 0.3 selection threshold is what matters downstream.

2. **Spatial-sequence analysis (Fig. 2d–f):** sort selective neurons by their peak-response position in leaf1; check whether the same ordering produces a matching firing *sequence* in leaf2. Correlate preferred positions across corridors (Pearson r). Low/zero correlation ⇒ not spatial coding. Guards against the classic "sort then find sequence" circularity by a two-stage split: neurons are *selected* on half of the leaf1/circle1 trials (train), and preferred positions are *read out* on the other half split into **odd vs. even trials** (and on held-out stimuli like leaf2, which were never used for selection). The cross-corridor and odd/even correlation values appear only in the figure panels; the Methods text gives no exact r values.

3. **Coding direction + similarity index (SI) (Figs. 2g–j, 3f–h):** build a population axis separating leaf1-selective vs. circle1-selective neurons (top 5% each, weights +1/N_trials, −1/N_trials, 0), fit on train trials, project **held-out** trials. Normalize each neuron by subtracting grey-space baseline and dividing by average corridor SD.
   `SI = (dx − dy)/(dx + dy)`, ranging −1…+1, measures whether a stimulus's projection looks "leaf-like" or "circle-like." Used to test whether new stimuli inherit the learned category axis, and to quantify **orthogonalization** (leaf2's projection onto the leaf1–circle1 axis shrinking after learning).

4. **Rastermap (Fig. 4a–d):** unsupervised visualization (Stringer et al. 2025, ref 39) that reorders neurons so nearby rows have similar activity, used as a **discovery tool** to spot task-related clusters — here, a group active only in the leaf1 (rewarded) corridor and switched off by reward.

5. **Reward-prediction index d′late vs early (Fig. 4e–n):** compares a neuron's activity on leaf1 trials where the cue/reward comes **late** vs. **early** in the corridor. Because stimulus drive and reward response are matched across early/late trials, this isolates **anticipatory** (expectation) activity. Reward-prediction neurons are selected by the d′late vs early ≥ 0.3 criterion (or, for Fig. 4a–d, via Rastermap clustering). Uses cue position (highly correlated with reward position; Fig. 1c) to split trials. The Methods describe no k-fold cross-validation for this readout; the reproducibility safeguards used across analyses are the train/test half-split for selecting neurons and odd/even trial splits for the coding-direction readouts (analysis 2–3 above).

6. **Retinotopy / area parcellation (Methods, Extended Data Fig. 1):** a **convolutional encoding model** of single-neuron responses to ≥500 natural images (×3 repeats). 200 shared 13×13 spatial kernels K fit by an EM-like alternation (assign each neuron a best position/kernel/amplitude, then re-fit K). Per-neuron preferred positions smoothed over nearest 50 neurons, then aligned to a reference mouse via **kriging interpolation** + an affine transform (grid search then gradient descent, regularized toward identity). Region borders drawn from the sign map, matched to Zhuang et al. 2017 (ref 33).

**Software:** Python 3, numpy, scikit-learn, Rastermap, matplotlib, Jupyter; MATLAB PsychToolbox-3 for stimuli; Suite2p; ScanImage.

**Statistics:** two-sided Student's t-tests, paired or independent as appropriate; significance thresholds *P<0.05, **P<0.01, ***P<0.001; **no correction for multiple comparisons** (explicitly stated); error bars = s.e.m. Exact p-values are tabulated in Methods.

---

## 10. Key Concepts and Definitions

* **Supervised vs. unsupervised learning.** Supervised = learning guided by labels/feedback (here, reward). Unsupervised = learning structure from inputs alone (here, mere visual exposure). *Central axis of the whole paper.*
* **Perceptual learning.** Long-lasting improvement in perceptual discrimination with practice; classically attributed to task-driven cortical plasticity — the interpretation this paper revises.
* **Higher visual areas (HVAs).** Cortical areas beyond V1 (medial/lateral/anterior groups here). The paper's spatial resolution across HVAs is a key strength.
* **Selectivity index d′.** Signal-detection measure of how distinguishable two response distributions are; here, corridor A vs. B. Bigger |d′| = more selective neuron.
* **Coding direction.** A population axis (weighted sum of neurons) along which two stimulus categories separate; projecting activity onto it reduces the population to one interpretable number per trial (Li et al. 2016, ref 37).
* **Similarity index (SI).** Normalized position of a stimulus's projection between the two category anchors; used to test generalization and orthogonalization.
* **Orthogonalization.** Two initially overlapping neural representations becoming more independent (less projection onto each other's axis) as fine discrimination is learned. Enables separating similar stimuli (leaf1 vs leaf2).
* **Reward-prediction signal.** Anticipatory neural activity that ramps up in expectation of reward and is suppressed when reward arrives — analogous to reward-prediction phenomena (Schultz et al. 1997, ref 40). Here found in anterior HVAs, task mice only.
* **Rastermap.** A discovery/visualization method that orders neurons by activity similarity to reveal population structure without a prior hypothesis.
* **Deconvolved calcium traces.** Estimated spiking activity inferred from slow GCaMP6s fluorescence; the analysis unit throughout. (Not literal spikes — a caveat.)
* **Unsupervised pretraining.** In ML, training on unlabeled data before the supervised task, which speeds/improves later learning; the biological analogue is tested behaviorally in Fig. 5.

---

## 11. Main Results

### Result 1: Most learning-related plasticity is unsupervised, and concentrated in medial HVAs
* **Finding:** After learning, many stimulus-selective neurons emerge in **medial** visual areas — and this increase occurs **similarly in task and unsupervised cohorts**, but **not** in the grating-exposure control (Fig. 1i,j; Extended Data Fig. 1d).
* **Evidence:** Fraction of selective (|d′|≥0.3) neurons rises significantly in medial region for both task (p=0.0073) and unsupervised (p=3.2×10⁻⁴) mice; grating cohort not significant. Robust to selectivity threshold (Ext. Fig. 1e) and holds for leaf1- and circle1-tuned neurons separately (Ext. Fig. 1f).
* **Supports hypothesis:** Yes — supports the unsupervised interpretation. **Strength:** strong and central, though based on modest n and a cross-cohort (not within-animal) manipulation of reward.
* **Nuance:** V1 showed little change in overall fraction of selective neurons (consistent with refs 34,35, differing from refs 10,13); a small medial-V1 selectivity decrease appeared in unsupervised mice.

### Result 2: The learned code is visual, not spatial
* **Finding:** Sorting medial neurons by firing sequence in leaf1 did **not** reproduce the sequence for leaf2; cross-corridor preferred-position correlations were near zero, whereas the odd/even control within leaf1 was near one (Fig. 2d–f; the paper shows these correlations in the figure panels and does not tabulate exact r values). But the **coding-direction/SI** analysis cleanly separated categories and **generalized** to new leaf2/circle2 stimuli in all regions and all cohorts including naive (Fig. 2i,j).
* **Evidence:** SI significant across regions in task, unsupervised, and naive mice (e.g., naive medial p=5.97×10⁻⁹). The visual readout matched the mice's behavioral generalization (they licked to leaf2, not circle2).
* **Supports:** Visual hypothesis strongly; spatial hypothesis rejected. **Strength:** convincing; the odd/even and held-out design guards against circularity.

### Result 3: Novelty responses in V1/lateral; orthogonalization everywhere (strongest medial)
* **Finding:** Newly introduced leaf2 drove a large **novelty** population in V1 and lateral areas that **shrank after further exposure** (adaptation), similarly in task and unsupervised cohorts (Fig. 3a,b). As mice learned to discriminate leaf1 vs leaf2, leaf2's projection onto the leaf1–circle1 axis was **reduced (orthogonalized)** vs. naive, in both cohorts, most strongly medial; no change in grating controls (Fig. 3d–h).
* **Evidence:** e.g., orthogonalization (Fig. 3h) unsupervised-vs-naive p=1.18×10⁻⁵ (medial); supervised-vs-naive p=0.002 (medial). Selectivity increase leaf1-vs-leaf2 significant medial only.
* **Supports:** Orthogonalization hypothesis; again largely reward-independent. **Strength:** solid, multi-measure.

### Result 4: A reward-prediction signal exists ONLY in supervised mice, in anterior HVAs
* **Finding:** Rastermap revealed a neuronal cluster active specifically in the rewarded (leaf1) corridor and **switched off by reward delivery**, located in **anterior HVAs** (Fig. 4a–d). Quantified with d′late vs early, these reward-prediction neurons were significantly enriched in anterior areas **in task mice after learning (p=0.0069) but not in unsupervised mice (p=0.708)** (Fig. 4f,g).
* **Evidence that it's expectation, not licking:** signal is suppressed after the cue while licking increases (Fig. 4i); it **ramps up seconds before the first lick** (Fig. 4j); and on unrewarded leaf2 trials it is higher when the mouse licks than when it doesn't (Fig. 4k, p=0.014) — trial-by-trial predictive of the animal's choice, unlike the medial population (Fig. 4l, p=0.180). Signal tracks reward expectation across sessions (absent in leaf3, present in swapped leaf1; Fig. 4m,n).
* **Supports:** The single clearly **supervised** component. **Strength:** strong and well-controlled (train/test–split neuron selection, multiple dissociations from licking).

### Result 5: Visual recognition memory becomes exemplar-specific; tied to visual position, not spatial memorization
* **Finding:** New leaf exemplar leaf3 was treated like the unrewarded leaf2 (mice withheld licking; neural projection biased toward the leaf2 axis) in both cohorts but not naive (Ext. Fig. 6). Spatially **swapped** leaf1 corridors were still recognized as leaf1 (mice licked normally), with neural vectors tracking the *visual* content at its new position — arguing against pure spatial/beginning-of-corridor memorization (Ext. Figs. 6–7).
* **Supports:** Emergence of detailed, visually-anchored recognition memory, again in both supervised and unsupervised conditions.

### Result 6 (behavioral, causal): Unsupervised pretraining accelerates task learning
* **Finding:** Mice pretrained 10 days on the **naturalistic** corridors (VRn) learned the subsequent rewarded discrimination **faster** than no-pretraining or **grating**-pretrained (VRg) mice (Fig. 5c–f).
* **Evidence:** Day-1 performance difference significant (VRn vs no-pretraining day-1 p=0.00493; VRn vs VRg day-2 p=0.0348). Learning gains largely **within-session** (Ext. Fig. 9). Not explained by differences in lick positions or trial counts (Fig. 5g,h).
* **Supports:** The functional prediction of the neural results. **Strength:** best-controlled, prospective, randomized arm; specificity vs. grating pretraining is important. **Caveat:** advantage is mainly early (days 1–2); all cohorts converge by day 5.

---

## 12. Figures and Tables Summary

*(No numbered tables; the paper is figure-driven. Exact p-values are listed in Methods rather than a table.)*

### Figure 1 — Plasticity after supervised and unsupervised training
* **Shows:** the VR task and timeline (a,b); example licking after learning (c,d); mesoscope field of view (e); d′ selectivity (f); single-neuron and population responses (g,h); 2D histograms of selective-neuron locations before/after in task and unsupervised mice (i); per-region % selective neurons across all three cohorts (j).
* **Interpret:** medial-region selectivity rises after learning in both task and unsupervised cohorts, not in grating controls.
* **Why it matters:** establishes the core "plasticity is unsupervised and medial" claim.

### Figure 2 — Visual vs. spatial coding on test stimuli
* **Shows:** test stimuli and licking generalization (a–c); sequence-sorting and cross-corridor position correlations (d–f); coding-direction construction and projections/SI (g–j).
* **Interpret:** sequences don't transfer (spatial rejected); coding axis generalizes to new stimuli and matches behavior (visual supported), even in naive mice.
* **Why it matters:** shows the learned representation is feature-based.

### Figure 3 — Novelty, adaptation, and orthogonalization
* **Shows:** novelty populations for leaf2 and their decrease with exposure (a–c); increased leaf1-vs-leaf2 selectivity in medial areas (d,e); example projections and the orthogonalization schematic and SI (f–h).
* **Interpret:** novelty in V1/lateral; representations orthogonalize as fine discrimination is learned, in both cohorts.
* **Why it matters:** mechanistic account of how a new stimulus is incorporated.

### Figure 4 — Reward-prediction signal in supervised training only
* **Shows:** Rastermap raster with behavioral annotations (a,b); anatomical location (c); population response suppressed by reward (d); d′late vs early definition (e); distribution and anterior enrichment (f,g); single-neuron generalization to leaf2 (h); dissociations from licking (i–l); persistence across sessions (m,n).
* **Interpret:** anterior HVAs carry a genuine reward-expectation signal present only with reward.
* **Why it matters:** identifies the one clearly supervised component and localizes it.

### Figure 5 — Unsupervised pretraining accelerates subsequent task learning
* **Shows:** design of three behavior-only cohorts (a,b); example and summary licking across days (c–f); first-lick distributions and trial counts (g,h).
* **Interpret:** naturalistic (not grating) unsupervised pretraining speeds learning, especially early, without confounding behavioral differences.
* **Why it matters:** turns a correlational neural story into a functional/causal behavioral demonstration.

### Extended Data (highlights)
* **ED Fig. 1:** retinotopy/convolutional-filter mapping; threshold-robustness; per-stimulus and V1 subdivisions.
* **ED Fig. 2:** running speeds comparable across cohorts and before/after (controls for arousal/locomotion confounds).
* **ED Fig. 3:** circle1 sequence analyses and coding projections across regions/cohorts.
* **ED Fig. 4:** coding direction does not simply track licking (early vs late cue trials).
* **ED Figs. 5–7:** novelty (circle2), exemplar-specific recognition memory (leaf3), swapped-corridor visual encoding.
* **ED Fig. 8:** reward- vs non-reward-prediction neurons; running/lick alignment controls.
* **ED Fig. 9:** within-day learning in the pretraining experiment.

---

## 13. Statistical and Quantitative Details

* **Neurons per session:** 20,547–89,577 (the abstract's "up to 90,000").
* **Animals:** 89 recordings / 19 imaging mice; 23 behavior-only mice.
* **Selectivity criterion:** |d′| ≥ 0.3.
* **Train/test discipline:** neuron selection on a train half of leaf1/circle1 trials, readout on the held-out half split into odd/even trials (sequence and coding-direction analyses); reward-prediction neurons selected by d′late vs early ≥ 0.3. No k-fold cross-validation is described in the Methods.
* **Tests:** two-sided paired or independent Student's t-tests; **no multiple-comparison correction** (authors' explicit choice — a limitation given the many region×cohort tests).
* **Representative p-values (from Methods):**
  * Fig. 1j medial: task p=0.0073; unsupervised p=3.21×10⁻⁴; grating n.s.
  * Fig. 2j medial SI: task p=2.94×10⁻⁴; unsupervised p=7.24×10⁻⁵; naive p=5.97×10⁻⁹.
  * Fig. 3h orthogonalization (medial): supervised-vs-naive p=0.002; unsupervised-vs-naive p=1.18×10⁻⁵; grating-vs-naive n.s. (0.705).
  * Fig. 4g anterior reward-prediction: task p=0.0069; unsupervised p=0.708.
  * Fig. 4k (leaf2 lick vs no-lick, anterior): p=0.014; Fig. 4l (medial control): p=0.180 (n.s.).
  * Fig. 5f VRn vs no-pretraining by day: 0.0049, 0.0056, 0.055, 0.259, 0.579 (early advantage that fades).
* **Complete per-region p-value tables (verbatim from Methods "Statistics and reproducibility").** Region order is **V1, medial, lateral, anterior** unless noted. These are reproduced in full here because they let an agent check whether any specific regional claim rests on a significant or a borderline/non-significant value — several do *not* survive per region.
  * **Fig. 1d** (anticipatory licking, before vs after): 0.714 (before), 5.97×10⁻⁴ (after).
  * **Fig. 1j** (% selective neurons): *task* 0.940, 0.00726, 0.0341, 0.0261; *unsupervised* 0.212, 3.21×10⁻⁴, [lateral/anterior not captured in this parse]. Grating cohort n.s. (Extended Data Fig. 1d). Note task lateral (0.034) and anterior (0.026) are nominally significant even though the paper's text emphasizes medial.
  * **Fig. 2f** (cross-corridor sequence correlation): *task* 7.97×10⁻⁶, 2.56×10⁻⁴, 1.84×10⁻⁵, 4.1×10⁻³; *unsupervised* 1.72×10⁻⁷, 1.04×10⁻⁴, 1.25×10⁻⁴, 3.07×10⁻³; *naive* 2.11×10⁻¹⁰, 1.25×10⁻⁵, 2.55×10⁻⁸, 8.66×10⁻⁶.
  * **Fig. 2j** (similarity index, new stimuli): *task* 0.0015, 2.94×10⁻⁴, 0.0020, 0.0013; *unsupervised* 1.72×10⁻⁴, 7.24×10⁻⁵, 2.44×10⁻⁴, 0.0082; *naive* 2.47×10⁻⁶, 5.97×10⁻⁹, 2.35×10⁻⁷, 2.73×10⁻⁶.
  * **Fig. 3b** (leaf2-vs-circle1 novelty distribution change): *task* 0.0037, **0.0922 (medial n.s.)**, 0.0026, 0.0136; *unsupervised* 2.34×10⁻⁵, 0.0081, 2.96×10⁻⁴, 0.0146.
  * **Fig. 3c** (licking to leaf2, new vs after): 0.0074.
  * **Fig. 3e** (leaf1-vs-leaf2 selectivity increase — *medial only*): *supervised vs naive* 0.991, 1.381×10⁻⁵, 0.352, 0.053; *unsupervised vs naive* 0.797, 4.45×10⁻⁶, 0.282, 0.727; *grating vs naive* 0.226, 0.284, 0.239, 0.570.
  * **Fig. 3h** (orthogonalization): *supervised vs naive* **0.084 (V1 n.s.)**, 0.002, 2.81×10⁻⁴, 6.2×10⁻⁷; *unsupervised vs naive* 5.26×10⁻⁵, 1.18×10⁻⁵, 9.32×10⁻⁵, 0.011; *grating vs naive* 0.316, 0.705, 0.375, 0.945 (all n.s.). (For supervised training the effect is actually *strongest* in lateral/anterior, not medial — the "most strongly medial" claim is the paper's, and holds most cleanly for the unsupervised cohort.)
  * **Fig. 4g** (anterior reward-prediction enrichment): task 0.0069, unsupervised 0.708. **Fig. 4k**: 0.014. **Fig. 4l** (medial control): 0.180 (n.s.).
  * **Fig. 5f** (Δlick response, day 1–5): *VRn vs no-pretraining* 0.00493, 0.00555, 0.0554, 0.259, 0.579; *VRn vs VRg* 0.538, 0.0348, 0.221, 0.541, 0.978; *VRg vs no-pretraining* 0.00782, 0.148, 0.415, 0.476, 0.510.
  * **Extended Data Fig. 9** (within-day learning, day 1–5): *VRn* 0.0166, 0.0033, 0.0120, 0.067, 0.1185; *VRg* 0.157, 0.0088, 0.188, 0.0356, 0.0230; *no-pretraining* 0.272, 0.0823, 0.0050, 0.0180, 0.0317.
* **Effect sizes / CIs:** Not reported as standardized effect sizes or confidence intervals — results are presented as group means ± s.e.m. with t-test p-values. *The paper does not provide formal effect-size estimates.* (The Nature reporting summary confirms this: it acknowledges effect sizes were not computed, no sample-size calculation was performed, no data were excluded, allocation was random, and investigators were not blinded because the task cohort required water restriction and training.)
* **Plain-English reading:** Very small p-values (e.g., 10⁻⁵–10⁻⁹) for the medial-region and coding-direction effects indicate the group differences are highly unlikely under chance given the samples; but with tiny n per cohort and no correction, individual borderline results (p≈0.01–0.05) should be read cautiously.

---

## 14. Interpretation

**Authors' interpretation.** Most cortical "learning" plasticity is unsupervised — a consequence of visual experience with natural image statistics, not of reward. The medial HVAs are the primary site; the code is visual and gets orthogonalized to support fine discrimination and recognition memory. A separate, genuinely supervised reward-prediction signal lives in anterior HVAs and could drive reinforcement learning. Functionally, the unsupervised representation is useful: it primes faster task learning, exactly as unsupervised pretraining does in artificial networks.

**Is it justified?** Largely yes for the *dissociation* claim, because the reward manipulation is clean and the effects replicate across measures (selectivity, sequences, coding direction, orthogonalization) and appear in the no-reward cohort. The reward-prediction localization is well controlled (multiple dissociations from licking). The functional claim (Fig. 5) is the strongest causal element because it is prospective and randomized.

**Alternative interpretations to keep in mind (critical):**
* *Exposure is not perfectly matched.* Task mice have extra experiences (water, cue–reward–position associations, stopping to drink). The authors exclude drinking timepoints, but attention/arousal/engagement likely still differ between rewarded and unrewarded cohorts. "Unsupervised" here means "reward-free," but attention can itself gate plasticity — so some of the shared plasticity could reflect shared *attentive exposure* rather than purely passive unsupervised learning.
* *Correlational neural claims.* The imaging results are associations between cohort and neural change; only Fig. 5 tests function. The paper does not manipulate the medial representation to show it is *necessary* for behavior.
* *Calcium-imaging proxy.* Conclusions rest on deconvolved GCaMP6s signals from excitatory neurons only; inhibitory circuits and fast dynamics are not directly observed.
* *Cross-sectional "naive" baselines.* Some before/after contrasts compare against separate naive animals rather than the same animals, adding between-animal variance.

Overall the conclusions mostly stay within the evidence, with the caveat that "unsupervised" should be read as "reward-independent," not "attention/experience-independent."

---

## 15. Strengths of the Paper

* **Clean conceptual manipulation.** Holding stimulus exposure ~constant while removing reward is the right design to dissociate supervised from unsupervised plasticity — a question the field had left correlational.
* **Scale and simultaneity.** Up to ~90,000 neurons across V1 and multiple HVAs at once allows **region-resolved** conclusions (medial vs. anterior vs. lateral) impossible with small recordings.
* **Convergent measures.** The same conclusion emerges from independent analyses (selectivity, sequence correlation, coding-direction generalization, orthogonalization), reducing the chance it's an artifact of one method.
* **Guards against circularity.** Neurons are selected on train trials and read out on held-out trials, with odd/even splits for the sequence and coding-direction analyses and generalization tested on stimuli never used for selection (leaf2/circle2) — the right family of controls for selection-based population analyses. *(Note: the paper relies on train/test and odd/even splits, not k-fold cross-validation.)*
* **A prospective, randomized functional test.** Fig. 5 elevates the paper from description to a causal behavioral claim, with a strong specificity control (grating vs. naturalistic pretraining).
* **Well-chosen controls.** Grating-exposure cohort isolates stimulus-specific from generic-VR effects; running-speed controls (ED Fig. 2) rule out locomotion confounds.
* **Discovery + confirmation.** Rastermap used to *find* the anterior signal, then a pre-specified index to *quantify* it — good practice.
* **Open data and code**, aiding reproducibility (and NMA use).

---

## 16. Limitations and Weaknesses

* **Small n per imaging cohort (3–9 mice)** with sex imbalance; several key p-values are borderline (0.01–0.05).
* **No multiple-comparison correction** despite many region×cohort×measure tests (authors state this explicitly). Some individual claims could be false positives.
* **Exposure not perfectly matched** between task and unsupervised cohorts (attention/engagement/associations differ) — "unsupervised" = reward-free, not experience-identical.
* **Correlational neural claims; no causal/perturbation test** of whether the medial unsupervised representation is *necessary* for behavior. Fig. 5 shows pretraining helps behavior but does not directly link the *specific* medial plasticity to the speed-up.
* **Calcium imaging proxy**, excitatory neurons only, deconvolved traces (0.75 s decay) — limited temporal resolution and cell-type coverage.
* **Pooling choices** (dark-reared mice pooled with normal; two swap types pooled; sessions counted as data points in some analyses) slightly inflate effective sample and could mask heterogeneity.
* **Area-border uncertainty.** Retinotopic parcellation is approximate and windows differ from the reference atlas; the authors argue combining areas into large regions mitigates this, but fine anatomical claims (e.g., exactly which HVA) carry uncertainty.
* **Pretraining benefit is transient** (mainly days 1–2; cohorts converge by day 5), so the functional effect, while real, is modest in magnitude/duration.
* **Naive-mouse baselines are cross-sectional** for some comparisons.

---

## 17. Assumptions Made by the Authors

* **Deconvolved GCaMP6s fluorescence approximates spiking activity** well enough for selectivity/coding analyses (standard but a proxy).
* **Restricting analysis to running periods equalizes arousal/engagement** across cohorts — assumes locomotion is a sufficient control for internal state (ED Fig. 2 supports comparable running, but engagement may still differ).
* **d′ ≥ 0.3 meaningfully identifies "selective" neurons** and results are threshold-robust (checked in ED Fig. 1e).
* **The coding-direction (linear) readout captures the behaviorally relevant representation.** A linear population axis is assumed adequate; nonlinear structure could carry additional information not tested.
* **Cue position is a valid proxy for reward position** in the d′late vs early analysis (justified by their high correlation).
* **Region borders from retinotopy + atlas alignment are accurate enough** to attribute effects to medial vs. anterior HVAs.
* **Cross-cohort comparison isolates reward's causal role**, i.e., cohorts differ *only* in reward/supervision to first approximation.
* **Mouse visual learning is an appropriate model** for general principles of supervised vs. unsupervised cortical representation learning (and by analogy for ANN pretraining).

Each assumption, if violated, most threatens the *strength* of the supervised/unsupervised dissociation rather than its direction — except the exposure-matching assumption, which if seriously violated could reattribute "unsupervised" plasticity to shared attentive experience.

---

## 18. Relationship to Computational Neuroscience

* **Computational framing:** The cortex is treated as a **representation-learning system**. The core question maps directly onto the ML distinction between **supervised** and **unsupervised/self-supervised** learning of representations.
* **Topics touched:** encoding (selectivity, coding directions), representation geometry (**orthogonalization**, generalization to new exemplars), **reward prediction / reinforcement learning** (anterior HVAs, Schultz-style prediction signals), and **transfer/pretraining** (unsupervised → faster supervised learning).
* **Mathematical frameworks used:** signal-detection d′; linear population coding axes and projections (Li et al. 2016); train/test–split neuron selection; a convolutional encoding model for receptive fields; kriging/affine spatial alignment.
* **Biology↔computation link:** It provides direct large-scale biological evidence for classic unsupervised-learning theories (sparse coding, predictive coding, slow-feature/free-energy) and for the modern practice of **unsupervised pretraining** (BYOL/BERT/GPT/DINO), suggesting the brain uses experience-driven representation learning that later accelerates task learning.
* **Character of the work:** primarily **descriptive + normative-adjacent** on the neural side (what representations exist and how they change) and **predictive/causal** on the behavioral side (pretraining accelerates learning). It is not a mechanistic circuit model; it invites future mechanistic (synaptic-plasticity) and normative (self-supervised objective) modeling.

**For NMA students:** this is a natural anchor for the big ideas of **predictive coding**, **generative models of neural activity**, **transfer learning**, and **generalization across stimuli/individuals** (Part 11 of the NMA guide). The dataset (PCA-compressed responses of up to ~80,000 neurons) is well suited to **linear/PCA-based population analyses** — start simple (tuning curves, d′, coding directions) exactly as the paper does.

---

## 19. Practical Implications

* **For neuroscience:** Reinterprets much perceptual-learning plasticity as experience-driven rather than task-driven; motivates always including an unrewarded-exposure control when claiming "task learning" changes.
* **For experimental design:** The reward-free exposure cohort is a template control; the odd/even + train/test–split neuron selection design is a model for avoiding circular population analyses (directly relevant to NMA's rigor guidance).
* **For AI/ML:** Adds biological support to unsupervised/self-supervised pretraining; the brain appears to do something analogous, with a functional benefit.
* **For theory:** Localizes candidate substrates — medial HVAs for unsupervised representation, anterior HVAs for reward prediction — that models can target.
* **Caution against over-claiming:** No clinical/BCI application is demonstrated; the pretraining benefit is modest and early. Applications to human perceptual training or education would be speculative extrapolation.

---

## 20. Future Research Directions

**Suggested by the authors:**
* Distinguish spatial vs. visual learning in the *same* circuits (e.g., hippocampus vs. visual cortex), since hippocampal representations may inherit visual properties (refs 44–46).
* Find **physiological substrates** (synaptic plasticity) for the observed changes and relate them to Hebbian/STDP rules or the behavioral-timescale plasticity rule (refs 29,30,47).
* Relate the unsupervised plasticity to classical unsupervised-learning theories and modern self-supervised methods (refs 14–19, 48–51).

**Additional (reviewer/independent) suggestions:**
* **Causal perturbation** (optogenetic/chemogenetic silencing of medial HVAs) to test whether the unsupervised representation is *necessary* for the faster learning in Fig. 5.
* **Larger cohorts** with balanced sex and **multiple-comparison correction** to firm up borderline effects.
* **Within-animal reward manipulation** (e.g., extinction/reinstatement) to reduce reliance on cross-cohort exposure matching.
* **Attention/engagement measures** (pupillometry, facemap) to test whether shared plasticity reflects shared attentive exposure vs. passive statistics.
* **Electrophysiology** to confirm the calcium-derived reward-prediction dynamics at spike-time resolution.
* **Direct model comparison:** fit self-supervised objectives (predictive/slow-feature/contrastive) to predict the observed medial-area representation changes.

---

## 21. Key Takeaways for Future Agents

* **Central claim:** Most learning-related plasticity in mouse visual cortex is **unsupervised** (driven by stimulus exposure, not reward), strongest in **medial HVAs**, follows **visual not spatial** rules, and **functionally speeds later task learning**; the one clearly **supervised** signal is a **reward-prediction ramp in anterior HVAs**.
* **Most important methods:** mesoscope 2-photon imaging of ~10⁴–10⁵ neurons; d′ selectivity; population **coding-direction / similarity index**; **d′late vs early** reward-prediction index (train/test–split neuron selection, not k-fold CV); Rastermap for discovery; a randomized behavioral **pretraining** experiment.
* **Most important results:** medial-area selectivity rises equally in task and unsupervised mice but not grating controls; coding axis generalizes to new stimuli; leaf2 representation orthogonalizes with fine learning; anterior reward-prediction signal only in task mice (p=0.0069 vs 0.708); naturalistic pretraining accelerates learning (day-1 p≈0.005).
* **Biggest caveat:** cohort comparison, not within-animal reward manipulation; exposure/attention only approximately matched; neural claims are correlational; small n; no multiple-comparison correction.
* **Remember:** "unsupervised" = **reward-free**, not attention-free.
* **Verify before citing as strong evidence:** whether a specific claim rests on a borderline p-value (0.01–0.05), whether it's the imaging (correlational) or behavioral (causal) arm, and the exact cohort n for that figure (n varies figure-to-figure).

---

## 22. Difficulty Guide

* **Beginner neuroscience student:** Abstract, Figs. 1 and 5, and the supervised/unsupervised framing are accessible. The coding-direction math, d′, and orthogonalization will need explanation. Start with Sections 2, 10, and 23 here.
* **Advanced undergraduate:** Can follow most of the main text; the retinotopy/kriging and train/test–split neuron selection in Methods are the hard parts (and are skippable for understanding the story).
* **Computational neuroscience student:** The natural audience — coding directions, d′, orthogonalization, and Rastermap are standard tools; the Methods are a good worked example of rigorous population analysis. This is an ideal NMA neurons-pod reference.
* **Machine-learning researcher:** The unsupervised-pretraining framing and Fig. 5 will resonate; the biological methods (GCaMP, Suite2p, HVAs) are the unfamiliar part. The encoding model (convolutional kernels, EM-like fit) is approachable.
* **Domain expert (visual cortex / plasticity):** Straightforward; the interesting scrutiny is on exposure-matching, area parcellation, and the strength of borderline effects.

---

## 23. "Explain Like I'm New" Summary

Imagine two groups of mice. Both walk (virtually) down the same hallways covered in "leafy" or "circley" wallpaper. **Group 1 gets a water reward** for licking in the leaf hallway — they're studying for a test. **Group 2 just strolls through the same hallways with no reward** — they're only sightseeing.

If you look at the brains, you'd expect only the studying mice (Group 1) to change, because they had a reason to learn. **But both groups' brains changed in almost the same way.** The neurons in a particular part of the visual brain (the "medial" areas) got much better at telling "leaf" from "circle" — in the sightseers too. So the change wasn't caused by the reward; it was caused by simply **seeing** the patterns a lot. That's *unsupervised* learning — learning from experience without being told the answers, like how you can recognize a friend's face without anyone ever grading you on it.

The brain did learn about the *look* of the patterns, not just *where* they appeared: when the researchers rearranged the patterns, the mice still recognized them by their leafy-ness. There was one thing only the reward group's brain had: a special group of neurons in the "front" visual areas that got excited **in anticipation of the water** and switched off once the water arrived — a little "reward is coming!" signal. That's the part that really needs the reward.

Finally, the punchline that computer scientists love: if you let mice sightsee first (unsupervised "pretraining") and *then* start the rewarded test, they **learn the test faster** — but only if they'd previously seen the actual test wallpaper, not some random stripes. This is exactly the trick used to build modern AI: show it tons of unlabeled data first, and it learns the real task faster afterward. The brain seems to use the same trick.

---

## 24. Technical Deep Dive

**Selectivity.** For corridors 1,2: `d′ = (μ₁ − μ₂)/((σ₁+σ₂)/2)` as written in the paper's Methods (average-of-SDs denominator; note this differs from the classic RMS pooled-SD d′, `√((σ₁²+σ₂²)/2)`), computed on deconvolved traces over 0–4 m during running; selective if |d′|≥0.3. Density maps: per-session 2D histograms of selective-neuron cortical positions, Gaussian-smoothed, normalized by total neurons, NaN where no cells recorded, then averaged across mice and aligned to a retinotopy-derived atlas.

**Coding direction.** Choose top-5% leaf1- and circle1-selective neurons on train trials. Normalize each neuron: `r_norm = (r − μ_grey)/√((σ²_leaf1+σ²_circle1)/2)`. Trial projection `v_proj^t = μ_leaf1 − μ_circle1` at each position — equivalent to weights (+1/N_leaf1, −1/N_circle1, 0) for positively/negatively/non-selective neurons. Evaluate only on held-out trials or other stimuli. Average within 0–4 m to get per-stimulus scalars a_leaf1, a_leaf2, a_circle1, a_circle2. **Similarity index** for a probe (e.g., leaf2): `dy = a_leaf1 − a_leaf2`, `dx = a_leaf2 − a_circle1`, `SI = (dx − dy)/(dx + dy) ∈ [−1,1]`. Orthogonalization = leaf2's projection onto the leaf1–circle1 axis shrinking after learning (Fig. 3h).

**Reward-prediction index.** Interpolate single-neuron activity by corridor position → trials×positions matrix. Split leaf1 trials into early- vs late-cue (cue position ≈ reward position). `d′late vs early = (μ_late − μ_early)/((σ_late+σ_early)/2)` (same average-SD denominator as the selectivity d′); select ≥0.3. Because early/late trials are matched on stimulus drive and reward response, the index isolates **anticipatory** activity. Neurons are selected by the d′late vs early ≥ 0.3 criterion; the paper's Methods describe **no** k-fold cross-validation for this readout (the reproducibility safeguards are the train/test half-split and odd/even splits used elsewhere). Dissociations from licking: temporal profile (suppressed at cue while licks rise; ramps before first lick) and choice-predictiveness on unrewarded leaf2 trials. Note two exclusions the Methods state explicitly: for the first-lick alignment (Fig. 4j), one mouse is dropped for having no trials with a first lick after 2 m; for the leaf2 lick vs. no-lick contrast (Fig. 4k,l), one mouse is dropped for having only one no-lick leaf2 trial.

**Retinotopy / encoding model.** Response of neuron n to image: `F_n(img) = a_n · (K_{k_n} ∘ img)(x_n, y_n)`, with K a 200×13×13 kernel bank. EM-like alternation: (1) brute-force assign each neuron its best (x,y,kernel,amplitude) by correlating kernel responses with neuron responses; (2) re-fit K given assignments (≈ averaging aligned linear RFs). ~<10 iterations to converge; kernels re-centered by center-of-mass each step. For new mice, smooth by averaging the max-correlation maps over nearest 50 neurons. Align to reference via **kriging** interpolation `f` (squared-exponential kernel, σ=200 µm) plus an affine transform A (grid-searched translation, then regularized gradient descent toward identity; determinant fixed if non-convergent). Borders from the visual-field sign map, matched to Zhuang et al. 2017.

**Statistics.** Two-sided paired/independent t-tests, no multiple-comparison correction, s.e.m. error bars; exact p-values tabulated (Methods). Notation reminder: μ = mean, σ = SD, r = Pearson correlation, d′ = discriminability, a_* = mean coding-axis projection for stimulus *.

---

## 25. Open Questions

Raised (or left open) by the paper:
* **Is the medial unsupervised representation *necessary*** for the faster task learning, or merely correlated? (No perturbation test.)
* **What synaptic/physiological rule** produces the changes (Hebbian, STDP, behavioral-timescale plasticity)?
* **Which self-supervised objective** best predicts the observed representation changes (predictive coding, slow features, contrastive)?
* **How separable are visual and spatial learning** in downstream circuits (hippocampus) that receive these visual signals?
* **Does attention/engagement**, rather than passive statistics, account for part of the shared plasticity? (Not directly measured.)
* **Why do V1 selective-neuron counts change in some studies but not here?** (Task/measurement differences hypothesized, not resolved.)
* **How general** is the effect beyond leaf/circle textures and mouse visual cortex — other modalities, species, more naturalistic tasks?
* **What is the full circuit** linking the anterior reward-prediction signal to the medial representation and to behavior?

---

## 26. Reliability Assessment

**Overall confidence:** **Moderate-to-High.**

* **Why:** The central dissociation is supported by multiple independent analyses that agree, sensible controls (grating exposure, running speed, train/test–split neuron selection, odd/even splits), a very large neural sample per animal, and — crucially — a **prospective randomized behavioral experiment** (Fig. 5) that gives the functional claim genuine causal weight.
* **Strongest evidence:** (1) medial-area unsupervised plasticity replicated across selectivity, coding-direction, and orthogonalization measures with very small p-values; (2) the anterior reward-prediction signal's multiple dissociations from licking; (3) the specificity of the pretraining benefit (naturalistic vs. grating).
* **Weakest evidence:** borderline p-values (0.01–0.05) on some region×cohort contrasts with small n and no multiple-comparison correction; cross-cohort (not within-animal) reward manipulation; correlational neural claims not tied by perturbation to the behavioral benefit.
* **Fragile assumptions:** exposure/attention matching between cohorts (if wrong, "unsupervised" is partly "shared attentive experience"); accuracy of area parcellation for fine anatomical attributions.
* **Replication:** The core qualitative claim (much plasticity is reward-independent; distinct anterior reward signal) is robust and worth treating as a strong, well-evidenced finding. Specific quantitative sub-claims and the exact anatomical localization would benefit from replication with larger cohorts and causal perturbations before being cited as settled.

---

## 27. Final One-Page Summary

**Problem.** Cortical neurons change with learning; this is usually assumed to be caused by the task (reward/feedback). Is that plasticity actually supervised, or would it happen from stimulus exposure alone (unsupervised)?

**Method.** Two-photon mesoscope imaging of 20,547–89,577 neurons/session across V1 and higher visual areas in mice running virtual-reality corridors, before and after learning. Compared task (rewarded) vs. unsupervised (same stimuli, no reward) vs. grating-exposure vs. naive cohorts, using d′ selectivity, population coding directions / similarity index, orthogonalization, Rastermap, and a reward-prediction index (d′late vs early, with train/test–split neuron selection) — plus a separate randomized behavioral pretraining experiment.

**Data.** 89 recordings / 19 GCaMP6s mice (imaging) + 23 mice (behavior-only). Naturalistic texture stimuli (leaf/circle/rock/brick), gratings, and novel/swapped exemplars. Open data (Janelia) and code (GitHub).

**Groups/comparisons.** Reward vs. no-reward (key manipulation); naturalistic vs. grating exposure (specificity); before vs. after learning; region-by-region (V1/medial/lateral/anterior); pretraining (naturalistic vs. grating vs. none).

**Main findings.** (1) Most learning-related plasticity appears in **both** task and unsupervised mice — it's unsupervised — and is strongest in **medial HVAs** (not in grating controls). (2) The code is **visual, not spatial**, and **orthogonalizes** as fine discriminations are learned. (3) A **reward-prediction ramp in anterior HVAs** appears **only** with reward and predicts trial-by-trial choice. (4) **Unsupervised pretraining on the task stimuli accelerates later task learning** (specific to naturalistic, not grating, pretraining).

**Interpretation.** Much "perceptual-learning" plasticity is experience-driven unsupervised representation learning; a separate supervised reward-prediction system sits in anterior areas. The brain benefits from unsupervised pretraining much as artificial networks do.

**Limitations.** Small n per imaging cohort; no multiple-comparison correction; cross-cohort (not within-animal) reward manipulation with only approximate exposure/attention matching; neural claims correlational (only the pretraining arm is causal); calcium-imaging proxy, excitatory neurons only.

**Why it matters.** It reframes a large literature (task-driven → largely experience-driven), localizes supervised vs. unsupervised substrates in cortex, and bridges biological plasticity with self-supervised/unsupervised pretraining in machine learning. For NMA, it is the reference paper for the Zhong et al. 2025 neurons-pod dataset and a clean template for rigorous, simple population analyses (d′, coding directions, PCA-space linear methods) with proper train/test discipline.
