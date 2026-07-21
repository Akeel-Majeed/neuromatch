# Method — Reward-Encoding Neurons across Learning

*Distilled from `method-flowchart.pdf`. **Primary method:** cross-validated
d′(late vs early cue), tracked across training days by region and cohort. The
per-neuron encoding-model **ablation** is retained as a single-session
validation. On the Zhong et al. 2025 data.*

## Goal

Track how the **proportion** and the **activation** (signal strength) of
**reward-encoding neurons** change across training days — broken down by brain
region and by cohort (supervised vs. unsupervised).

## Why the method changed from the proposal

The proposal specified the encoding-model **ablation** both to classify reward
neurons and to track their proportion across days. We kept the ablation as a
one-session validation but switched the **across-days tracking to a
cross-validated d′(late vs early cue)**, for two reasons:

1. **Cross-cohort fairness.** The ablation keys off *water delivery*, which does
   not exist in the unsupervised cohort — so unsupervised would score zero *by
   construction*, a circular result. d′ keys off the **sound cue** (whose position
   tracks the reward zone) and the cue exists with or without water, following the
   authors' own `utils.py`. This makes supervised-vs-unsupervised a fair test.
2. **Comparability.** d′(late vs early), `|d′| ≥ 0.3`, is Zhong et al.'s own
   definition of a reward-prediction neuron (their Fig. 4f–g), so our per-region
   percentages line up with the paper.

## Inputs (shared)

- **Neural data:** up to ~80k neurons, provided SVD(400-PC)-compressed; we
  reconstruct a large sample **per region** (V1 · medial · lateral · anterior),
  much larger than the earlier 1,000-neuron pilot.
- **Behavior:** sound-cue position (≈ reward-zone position), trial structure,
  corridor position, running.

## Primary pipeline — d′(late vs early cue), across days

1. **Sample neurons** per region per mouse (capped at what each region has).
2. **Reward-zone activity.** For each rewarded-corridor (leaf1) trial, take each
   neuron's mean activity in the reward zone (5–40 dm).
3. **Split trials** by cue position: early-cue vs late-cue. The cue tracks reward,
   and exists in both cohorts.
4. **Cross-validated d′** (per neuron): split the trials into two interleaved
   folds and compute `d′ = 2(μ_late − μ_early)/(σ_late + σ_early)` in each.
5. **Classify (flag).** A neuron is reward-encoding if `|d′| ≥ 0.3` in **both**
   folds with the **same sign**. Cross-validation is essential: a single-pass
   `|d′| ≥ 0.3` on a few dozen trials is cleared by noise ~a third of the time;
   requiring both folds to agree collapses that false-positive rate.
6. **Activation (strength).** For *all* sampled neurons (unbiased), record the
   mean `|d′|` across folds — how strongly the neuron tracks reward timing.
7. **Aggregate — the mouse is the replicate.** Per mouse, compute the **percentage
   of reward-encoding neurons** (how many) and the **mean d′** (how strongly),
   then take mean ± s.e.m. **across mice**, for each stage × region × cohort.
   Neurons within a mouse are *not* independent replicates.
8. **Shuffle floor.** Scramble the late/early labels, rerun the *same*
   cross-validated test, and average — the chance % expected from noise.

## Validation — encoding-model ablation (one session)

A single-session check that the reward signal is real beyond the cue index:

1. Build a design matrix X (stimulus, position bases, velocity, reward & cue lag
   bases). Fit a per-neuron ridge model on train trials.
2. **Ablate the reward block and refit**; the rise in held-out MSE
   (`ΔMSE = error_reduced − error_full`) is reward's unique contribution.
3. **Permutation test** on reward timing → `p`; a neuron is a candidate if
   `ΔMSE > 0` and `p < 0.05`.

### Ablation note — zero-out first, refit to confirm

- **Zero-out (fast screen):** keep the fitted weights, set the reward input to 0
  at inference. Cheap, but with stimulus weights frozen they can't absorb reward's
  share, so it **over-credits reward** — treat a hit as a *candidate* only.
- **Refit (confirm):** drop the reward column and re-estimate the weights so
  stimulus/position/velocity can compensate. This is the honest unique-variance
  test. The permutation test does not rescue the zero-out inflation (shuffling
  reward breaks the stimulus–reward correlation, so the null can't see it).

## Rigor / controls

- **Cross-validation:** the effect must reproduce in both trial folds.
- **Shuffle null** on the late/early labels (chance floor for the proportion).
- **Cue-based reward event** — fair across cohorts (water is not required).
- **Mouse as the replicate** — error bars are across mice, not neurons.
- **Skip + report** any session with no cue-position variation or too few trials.
- (Ablation track) position and velocity as nuisance regressors guard against a
  motor confound.

## Interpretation

Support for the reward-prediction account looks like: the proportion *and*
activation sit clearly **above the chance floor**, **rise** before→after learning,
are concentrated in **anterior HVAs**, and appear in the **supervised** cohort
only — the unsupervised cohort should stay near the floor. Because d′(late vs
early) flags any reproducible late/early difference (broader than a *proven*
anticipatory ramp), treat a hit as "worth the follow-up," not proof.
