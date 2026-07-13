# Project Meeting — Neural Encoding of Reward

*Discussion with Esteban (supervisor/collaborator). Project 2 of 2 — Esteban considers this the more doable option given time constraints.*

## Meeting Context

- Focus: a linear regression (encoding) model to identify **reward-encoding neurons** and track how they change across training days.
- Dataset: Zhong et al. 2025 — mouse visual cortex, 2-photon calcium imaging, supervised (task) vs. unsupervised cohorts.

## Linear Regression Model for Firing Rate

- **Goal:** predict a neuron's firing rate from task variables to identify reward-encoding neurons.
- **Neural data:** neurons × time, values = fluorescence (ΔF/F, a proxy for firing rate).
- **Target `y`:** firing rate (fluorescence) for a single neuron — one model fit per neuron.
- **Design matrix `X`** encodes all variables of interest per time bin:
  - Stimulus type (leaf vs. circle — binary encoding)
  - Animal position in corridor
  - Animal velocity
  - Reward presence

## Training and Test Pipeline

1. Discretize ΔF into time bins, take the mean per bin.
2. Split **trials** 80% train / 20% test.
3. Fit θ (weights) on the training set (least squares = Gaussian MLE).
4. Run inference on the test set using the fixed θ.
5. Error metric: `y − ŷ` (ground truth vs. predicted) on held-out data.

## Identifying Reward-Encoding Neurons

- **Omission method (Esteban's preference):** remove the reward variable from `X`, refit/recompute `ŷ`. If test error **increases**, the neuron encodes reward (its omission degrades model fit).
- **Two-model method (Akeel's suggestion):** fit one model with reward and one without, compare directly.
- Both are valid and near-equivalent; Esteban prefers the omission framing.

## Statistical Validation: Permutation Test

- Per neuron, compute observed difference `d` = error(without reward) − error(with reward).
- Shuffle labels 1,000× and recompute `d` each time to build a null distribution.
- p-value = proportion of shuffled `d` values exceeding the true `d` (e.g., 1/1,000 → p = 0.001).
- **Key insight:** a smaller raw `d` can be more statistically meaningful than a larger one, depending on the spread of the null.

## Research Questions and Next Steps

- **Core question:** how does the proportion of reward-encoding neurons change across training days (day 1 vs. 2 vs. 3…), plotted over time and broken down by brain region?
- Compare **supervised vs. unsupervised** conditions.
- Compare across **stimulus types** (leaf vs. circle).

## Open Questions / Dependencies

- **Reward timing:** the reward regressor requires per-trial reward/cue timing. Confirm this is in the data release (ask Project TA) before committing — it is the gating dependency.
- **Permutation null:** to isolate reward *specifically* (stimulus and reward are correlated by task design), shuffle the **reward column of `X`** rather than the whole `y`. Shuffling `y` tests "is this neuron task-related at all"; shuffling the reward column tests "does reward carry unique variance beyond the other regressors" — the actual claim.
- **Interpretation asymmetry:** a significant result is trustworthy; a null is ambiguous (reward may matter but be too collinear with stimulus to separate).
