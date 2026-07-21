# Method — Reward-Encoding Neurons across Learning

*Distilled from `method-flowchart.pdf`. **Primary method:** encoding-model
**reward ablation** (full vs reward-block-removed ridge refits + reward-timing
permutation test), tracked across training days by region, in the **supervised
cohort**. On the Zhong et al. 2025 data.*

## Goal

Track how the **proportion** and the **activation** (signal strength) of
**reward-encoding neurons** change across training days — broken down by brain
region — in the supervised cohort.

## Why the method changed (again)

An earlier revision of this document switched the across-days tracking from the
ablation to a cross-validated d′(late vs early cue), chiefly for cross-cohort
fairness: the cue exists with or without water, so supervised and unsupervised
mice could be compared on the same index. We have now migrated back to the
**reward ablation** as the primary measure, for one decisive reason:

- **Specificity.** d′(late vs early) flags *any* reproducible difference between
  late- and early-cue trials — broader than reward encoding. The ablation asks
  the sharper question: does removing the reward block hurt held-out prediction
  *after* position, speed, stimulus, licks and cue have had their chance to
  compensate, and does a permutation test on reward timing confirm it? That is
  the direct test that a neuron **specifically encodes reward**.

The cost, accepted explicitly:

- **The unsupervised cohort is dropped.** The ablated regressor is *water
  delivery*; unsupervised mice receive none, so their ablation would score zero
  **by construction** — a circular result. The supervised-vs-unsupervised
  contrast is not tested by this analysis; the question is instead how reward
  encoding evolves across learning within the supervised cohort.

## Inputs (shared)

- **Neural data:** up to ~80k neurons, provided SVD(400-PC)-compressed; we
  reconstruct a balanced sample **per region** (V1 · medial · lateral ·
  anterior) per mouse.
- **Behavior:** frame-aligned trial structure, corridor position, running,
  stimulus, lick, cue and **water-reward** event times.

## Single-session pilot (Part A)

One supervised after-learning session, run deep as a methods check: 750 neurons
per region, the full expanded design matrix, grid-searched ridge alpha, 199
permutations, zero-out vs refit comparison, and per-region candidate summaries.
This validates the machinery that Part B then scales.

## Primary pipeline — reward ablation across days (Part B)

Per session (supervised cohort; `train1`/`train2`, each before vs after
learning), per mouse:

1. **Sample neurons** per region per mouse (default 250, capped at what each
   region has) and reconstruct only those from the SVD.
2. **Design matrix.** Stimulus identity; position bases; position×stimulus;
   speed, movement, acceleration; reward, lick and cue lag bases; epochs;
   landmarks. Standardized with a scaler fit on **training frames only**.
3. **Split trials** odd/even (matches Zhong's supplied `ft_trInd_odd/even`).
4. **Full vs reduced refits** at a fixed ridge alpha (`PART_B_ALPHA`, default
   1.0 — grid search is skipped for runtime). Fit the full model on odd trials;
   refit without the reward block; score both on even trials.
   `ΔMSE = MSE_reduced − MSE_full` is reward's unique held-out contribution.
5. **Permutation test.** Shuffle reward-time offsets among rewarded trials
   (default 50 permutations), rebuild only the reward columns, refit, and
   collect the null ΔMSE. Candidate: `ΔMSE > 0` **and** `p < 0.05`.
6. **Proportion + activation.** Per (mouse, region): the **percentage of
   candidates** (how many) and the **mean ΔMSE over all sampled neurons**
   (how strongly; unbiased by selection).
7. **Aggregate — the mouse is the replicate.** Mean ± s.e.m. **across mice**
   per stage × region. Neurons within a mouse are *not* independent replicates.
8. **Chance floor.** The nominal 5% false-positive rate of the per-neuron
   `p < 0.05` permutation test, drawn as a reference line — the signal is the
   per-mouse *proportion* above that floor.

**Runtime budget.** Defaults (2 mice/stage, 250 neurons/region, 50
permutations, fixed alpha) size Colab **Run all** at roughly 20 minutes; raise
`MAX_MICE_PER_CONDITION`, `N_PER_REGION_OVERTIME`, or
`N_PERMUTATIONS_OVERTIME` for more power.

### Ablation note — zero-out first, refit to confirm

- **Zero-out (fast screen):** keep the fitted weights, set the reward input to 0
  at inference. Cheap, but with stimulus weights frozen they can't absorb reward's
  share, so it **over-credits reward** — treat a hit as a *candidate* only.
- **Refit (confirm):** drop the reward column and re-estimate the weights so
  stimulus/position/velocity can compensate. This is the honest unique-variance
  test, and the one both parts use for classification. The permutation test does
  not rescue the zero-out inflation (shuffling reward breaks the stimulus–reward
  correlation, so the null can't see it).

## Rigor / controls

- **Permutation null** on reward timing — the classifier itself is inferential,
  so no separate label-shuffle floor is needed; the nominal floor is 5%.
- **Refit, not zero-out**, for every classification decision.
- **Supervised cohort only** — water-based ablation is undefined (zero by
  construction) for unsupervised mice.
- **Mouse as the replicate** — error bars are across mice, not neurons.
- **Skip + report** any session with too few reward events (< 10) or too few
  trials to split.
- Position and velocity as nuisance regressors guard against a motor confound.

## Interpretation

Support for the reward-learning account looks like: the proportion *and*
activation sit clearly **above the 5% nominal floor** and **rise** before→after
learning, concentrated in **anterior HVAs**. Because candidates carry no
multiple-comparison correction across neurons and a fixed ridge alpha is used
for speed, treat borderline percentages near the floor as noise, and treat a
hit as "worth the follow-up," not proof.
