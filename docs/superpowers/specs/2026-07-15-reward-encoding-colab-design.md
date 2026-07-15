# Reward-Encoding Pilot Colab Design

## Purpose and success criteria

Create one self-contained Google Colab notebook that tests the proposed reward-encoding method on Zhong et al.'s supervised after-learning session `VR2_2021_04_06_1`. A fresh Colab CPU runtime must be able to run the notebook top to bottom without manual data uploads, construct and validate the expanded design matrix, fit regularized per-neuron encoding models, compute held-out MSE and R², quantify reward importance with zero-out and refit ablations, run a trial-wise permutation test, and export neuron-level results.

This is a one-mouse, one-session feasibility pilot. It may identify candidate reward-encoding neurons, but it must not present neuron-level percentages as animal-level or longitudinal evidence.

## Data and sampling

- Download the behavior, SVD-decomposed neural activity, and retinotopy files directly from Figshare using the file IDs already used by Zhong's tutorial notebook. Downloads are cached under `/content/Zhong_et_al_2025` and validated before analysis.
- Load `Beh_sup_train1_after_learning.npy`, session key `VR2_2021_04_06_1`; `VR2_2021_04_06_1_SVD_dec.npy`; and `VR2_2021_04_06_trans.npz`.
- Map `iarea` values to `V1=8`, `mHV={0,1,2,9}`, `lHV={5,6}`, and `aHV={3,4}`. Ignore unmapped values `-1` and `7`.
- With NumPy RNG seed 42, sample 250 neurons without replacement from each mapped region. Sampling is independent of neural activity and produces a fixed 1,000-neuron pilot.
- Reconstruct only the selected neurons as `U[:, selected_indices].T @ V`, yielding frames × neurons after transposition. Do not reconstruct the full 71,069-neuron matrix.
- Align neural and behavioral arrays by neural frame. Raise a descriptive error if their lengths differ rather than silently truncating. Retain finite frames assigned to a trial; the design matrix controls for movement and corridor/gray epochs, so both moving and stationary within-trial frames remain eligible.

## Design matrix and model

Build the expanded matrix described by `docs/design-matrix-flowchart.pdf`, using only frame-aligned behavior variables. Include an intercept and retain a column-to-block manifest.

- Stimulus: one-hot `ft_WallID` columns for observed corridors.
- Position: 12 overlapping raised-cosine basis functions across corridor position 0–60, plus position×stimulus interactions.
- Movement: z-scored running speed, five raised-cosine speed bases, `ft_isMoving`, and z-scored acceleration derived from `ft_RunSpeed`.
- Reward: eight raised-cosine event bases spanning −3 to +3 seconds around finite `RewardFr` events, so the block covers anticipation and delivery-related changes.
- Lick: eight event bases spanning −1 to +2 seconds around `LickFr` events.
- Cue: eight event bases spanning 0 to +3 seconds around `SoundDelayFr` (fall back to `SoundFr` only if the delayed field is absent).
- Epochs: `BefCueFr`, `AftCueFr`, `ft_GraySpc`, and `ft_CorrSpc` booleans.
- Landmarks: six causal event bases spanning 0 to +2 seconds for each of `StartFr`, `GrayFr`, and `EndFr`.

Generate event bases from seconds using the median finite interval in `beh['ft']`; never assume a frame rate. Fit transforms using odd-trial training rows only: remove non-finite/constant columns, then standardize non-binary columns and reuse those parameters on even-trial rows. Assert that train/test trial IDs are nonempty and disjoint.

Fit multi-target ridge regression, one coefficient vector per neuron. Tune one shared alpha from `10**[-2, -1, 0, 1, 2, 3]` using three grouped folds of odd trials and mean validation MSE across neurons. Refit the selected alpha on all odd-trial frames. Report per-neuron held-out MSE and R² on even trials.

## Reward attribution and inference

- **Zero-out screen:** keep full-model coefficients fixed, set the standardized reward block to its reward-absent value on the even-trial matrix, and compute `delta_mse_zero = mse_zero - mse_full`. Label this descriptive because correlated predictors cannot compensate.
- **Refit confirmation:** remove the reward block, refit ridge with the same alpha on odd trials, and compute `delta_mse_refit = mse_reduced - mse_full` and `delta_r2_refit = r2_full - r2_reduced` on the same even trials. This is the primary unique-variance effect.
- **Permutation null:** perform 199 permutations by shuffling observed reward event times among rewarded trials, preserving one event per originally rewarded trial and the reward–stimulus relationship while breaking exact timing. Rebuild only the reward block, apply the training-derived transform, refit with the fixed selected alpha, and recompute held-out `delta_mse_refit` for all neurons. Use deterministic seed 42 and the corrected one-sided value `(1 + count(null >= observed)) / 200`.
- Classify a candidate as reward-encoding when observed `delta_mse_refit > 0` and raw permutation `p < 0.05`, per the user's selected rule. Show an explicit warning that 1,000 uncorrected tests can yield false positives and that no mouse-level inference is possible.

The zero-out calculation must not determine which neurons receive permutations; all 1,000 neurons are tested to avoid selection-biased p-values. A configuration cell may lower permutations for debugging or increase them for a longer run, but 199 is the default Colab setting.

## Notebook outputs and failure handling

The notebook displays:

1. Download and data-validation summary, including shapes, trial counts, event counts, region counts, frame rate, and train/test sizes.
2. Design-matrix block manifest, final matrix shapes, example feature traces, and a compact feature-correlation diagnostic.
3. Alpha cross-validation curve and full-model held-out MSE/R² distributions.
4. Zero-out versus refit ΔMSE scatter, observed-versus-null examples, and reward-kernel coefficients for representative candidates.
5. Candidate counts and raw percentages by region with binomial confidence intervals, clearly labeled as descriptive for one session.
6. A downloadable `reward_encoding_pilot_results.csv` containing neuron index, region, full/reduced metrics, both ablation effects, raw p-value, candidate flag, and reward coefficients; plus a JSON run manifest containing configuration and data identifiers.

Downloads use streamed requests with timeouts, status checks, temporary `.part` files, and atomic rename. Before fitting, the notebook raises actionable errors for missing behavior fields, corrupt downloads, insufficient neurons in a region, invalid event indices, empty/disjoint split failures, non-finite matrices, or sessions with no reward events. Random seeds and package versions are printed for reproducibility.

## Verification and acceptance tests

- Validate notebook JSON and execute all data-independent helper/synthetic-test cells outside Colab.
- Synthetic recovery test: injected reward-related activity must produce positive refit ΔMSE and a smaller p-value than null neurons; a nuisance-only target must not systematically benefit from reward omission.
- Unit checks cover event-basis alignment at boundaries, seconds-to-frame conversion, region mapping, balanced sampling, trial leakage, training-only scaling, reward-absent zero-out values, MSE/R² formulas, corrected permutation p-values, and output schema.
- Run the complete notebook from a clean environment against the real Figshare session, with 1,000 neurons and 199 permutations, and verify that every cell completes, all expected figures/tables are produced, CSV/JSON exports are readable, peak memory stays within a free Colab CPU runtime, and elapsed time is reported. If the exact Colab service is unavailable during development, execute the same notebook kernel locally with the downloaded files and state that environmental limitation rather than claiming browser verification.

## Assumptions

- Zhong's SVD reconstruction is the available after-learning neural target and is suitable for this feasibility test; it is not raw fluorescence.
- The expanded design matrix and ridge model supersede the earlier four-predictor OLS sketch, while MSE remains the requested primary prediction-error metric.
- Odd/even trial splitting follows Zhong's supplied masks and the design-matrix flowchart, superseding the older 80/20 wording.
- Raw `p < 0.05` is retained by user choice despite the multiple-testing caveat.
