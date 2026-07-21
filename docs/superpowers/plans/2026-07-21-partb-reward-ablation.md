# Part B Migration: d′ → Reward Ablation (supervised only)

> Execute with superpowers:executing-plans. User decisions (2026-07-21):
> ablate the **water-delivery reward block** (Part A's method), **supervised
> cohort only** (unsupervised get no water → ablation would be zero by
> construction, and the research aim is tracking reward-encoding neurons across
> learning, not the cohort contrast). Part B must finish **Run-all in ~20 min**
> on Colab; shrink the dataset/settings accordingly. Work directly on `master`
> (explicit user override, no worktree, no commits).

**Goal:** In `src/reward_encoding_pilot_colab.ipynb`, replace Part B's
cross-validated d′(late vs early cue) measure with the encoding-model **reward
ablation** from Part A (full vs reward-block-removed ridge refits + reward-timing
permutation test), run per mouse across the four supervised learning stages.

**Files:**
- Modify: `tests/test_reward_encoding_notebook.py` (tests first)
- Modify: `src/reward_encoding_pilot_colab.ipynb` (cells edited programmatically
  by id, JSON round-trip with `indent=1, ensure_ascii=False`)

### Task 1: Tests for the new Part B contract
- [x] Add `test_part_b_uses_reward_ablation`: asserts `reward_ablation_session`
  exists in source, `DPRIME_THRESHOLD` / `_reward_encoding` / `Beh_unsup` are
  gone, and `N_PERMUTATIONS_OVERTIME` is present.
- [x] Run `.venv/bin/python -m pytest tests/test_reward_encoding_notebook.py -q`;
  expect the new test to FAIL, all existing tests to PASS.

### Task 2: Rewrite Part B cells in the notebook
- [x] Cell `reward-pilot-003` (config): drop `DPRIME_THRESHOLD`,
  `N_SHUFFLES_OVERTIME`, `REWARD_ZONE_DM`; drop unsupervised rows from
  `OVERTIME_CONDITIONS`; add `N_PER_REGION_OVERTIME = 250`,
  `MAX_MICE_PER_CONDITION = 2`, `N_PERMUTATIONS_OVERTIME = 50`,
  `PART_B_ALPHA = 1.0` (fixed alpha — skips per-session grid search for the
  20-min budget); update the trailing print.
- [x] Cell `reward-pilot-000` (intro): Part B paragraph now describes the
  ablation over supervised mice; note unsupervised exclusion rationale.
- [x] Cell `f6454490`: keep `fetch_manifest` / `download_by_name`; delete
  `_dprime_between` and `_reward_encoding`.
- [x] Cell `2472c3c7`: replace `reward_dprime_session` with
  `reward_ablation_session(beh, mouse, manifest, ...)` — per mouse: download
  SVD+retinotopy by name, `balanced_sample` + `reconstruct_selected`,
  `align_behavior_frames`, `odd_even_masks`, `build_design_matrix`, train-only
  `StandardScaler`, `fit_reward_models` at `PART_B_ALPHA`,
  `reward_permutation_null` with `N_PERMUTATIONS_OVERTIME`, candidates =
  `delta_mse_refit > 0 & p < 0.05`; return per-region flag + strength
  (`delta_mse_refit`) arrays. Skip sessions with < 10 reward events.
- [x] Cell `036eebd6`: aggregation loop over supervised-only conditions;
  `pct_reward` (candidate proportion) and `mean_delta_mse` (activation
  strength) per (mouse, region); nominal 5% chance reference instead of the
  shuffle floor; keep `skipped` reporting.
- [x] Cell `bc917351`: figure — single supervised series, top row % candidates
  with dashed 5% nominal line, bottom row mean ΔMSE; dots = mice, mean ± s.e.m.
  across mice; keep `reward_encoding_over_time.csv` export.
- [x] Cell `4138ada8` (§8 markdown): rewrite — ablation definition, why
  supervised-only (water doesn't exist for unsupervised → zero by construction),
  nominal 5% floor, mouse-as-replicate, 20-min budget knobs.
- [x] Cell `reward-pilot-024` (interpretation checklist): update Part B bullets.

### Task 3: Verify
- [x] Run full pytest suite in `.venv`: all PASS.
- [x] `python3 -m json.tool` on the notebook; confirm only intended cells
  changed (git diff cell ids).
- [x] Note honestly: the real-data end-to-end run (several GB of Figshare
  downloads) cannot be executed in this environment — user runs Run-all in Colab.

### Out of scope (flag to user at the end)
- `docs/method.md` still describes d′ as the primary across-days method and
  ablation as single-session validation — now stale; offer to update.
