# Method — Identifying Reward-Encoding Neurons

*Distilled from `method-flowchart.pdf`. Per-neuron linear encoding model with an omission test and permutation validation, on the Zhong et al. 2025 data.*

## Goal

Identify **reward-encoding neurons** and track how their proportion changes across training days — broken down by brain region, cohort (supervised vs. unsupervised), and stimulus type (leaf vs. circle).

## Inputs

- **Neural data:** neurons × time, ΔF/F fluorescence (a proxy for firing rate).
- **Design matrix X** (time × variables): stimulus type (leaf/circle, binary), position in corridor, velocity, and reward presence.

## Pipeline

1. **Preprocess.** Bin ΔF/F into time bins, take the mean per bin, and align the neural data and X on the same time axis.
2. **Split by trial.** 80% train / 20% test — split by *trial*, not by bin, because bins within a trial are correlated and would otherwise leak.
3. **Fit the full model** (one per neuron): `y = Xθ`, estimating θ by least squares (Gaussian MLE) on the training trials.
4. **Full test error.** Predict ŷ on the held-out 20%; `error_full = MSE(y, ŷ)`.
5. **Omission / ablation.** Remove the reward regressor, refit, and predict again to get `error_reduced` on the same held-out trials.
6. **Effect size (per neuron).** `d = error_reduced − error_full`. A positive d means reward improved the fit.
7. **Permutation test.** Shuffle the reward column across trials, refit, and recompute d; repeat ~1,000× to build a null distribution of d.
8. **p-value.** `p = fraction of shuffled d ≥ true d`. A small but steady d can beat a large noisy one — significance is d relative to the spread of its null, not its raw size.
9. **Classify.** A neuron is "reward-encoding" if `p < threshold`.
10. **Aggregate.** Compute the proportion of reward-encoding neurons across training days, by brain region, supervised vs. unsupervised, and leaf vs. circle.

## Rigor / controls

- Train/test split, applied reflexively.
- Permutation null built by shuffling the **reward column** (isolates reward's *unique* variance beyond the other regressors).
- **Position and velocity as nuisance regressors** — reward has to explain variance beyond running and location, guarding against a motor confound.
- **Cross-cohort check:** the signal should vanish in the unsupervised cohort (same stimuli, no reward).

## Interpretation

A **significant** d is trustworthy reward attribution. A **null** d is ambiguous — reward may still matter but be too collinear with stimulus to separate (reward occurs only in the leaf corridor, so the two travel together). Treat nulls with that caveat rather than as clean evidence of "no reward encoding."

### Method note — reward ablation: zero-out first, refit to confirm

Per-neuron linear encoding model (full method in `project-meeting.md` / `method-flowchart.pdf`):
predict each neuron's ΔF/F from stimulus + position + velocity + reward, then remove reward
and see if test error rises. Two ways to remove reward:

- **Zero-out (try FIRST):** keep the fitted weights, set the reward input to 0 at inference.
  Cheap — fit the full model once, get the ablated prediction for free. Good fast screen over a
  **small subset** of neurons (we are NOT running all ~90k). Downside: with the fitted stimulus
  weights frozen, they can't absorb reward's share.
- **Refit (do SECOND, to confirm):** drop the reward column and re-estimate the weights, so
  stimulus/position/velocity can compensate. This is the honest "unique variance" test.

**Why both:** reward and stimulus are correlated in the task (reward only in the leaf corridor),
so zero-out **over-credits reward** — it can flag a neuron as reward-encoding when stimulus alone
would explain it. So treat a zero-out hit as a *candidate* only, and re-test it with the refit
before believing it. The permutation test does not rescue this (shuffling reward breaks the
correlation, so the null can't see the inflation). Also confirm reward is coded {0,1} — zero only
means "reward absent" if the off-state is genuinely 0.

**A vs B in one line:** A = measure how much of the change is reward-free (shared), by region.
B = find and localize the change that only reward produces.