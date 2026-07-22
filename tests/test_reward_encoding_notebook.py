from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "src" / "reward_encoding_pilot_colab.ipynb"


def load_notebook() -> dict:
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def source_text() -> str:
    return "\n".join("".join(cell.get("source", [])) for cell in load_notebook()["cells"])


def helper_namespace() -> dict:
    namespace: dict = {}
    for cell in load_notebook()["cells"]:
        if "unit-testable" in cell.get("metadata", {}).get("tags", []):
            exec("".join(cell["source"]), namespace)
    return namespace


def test_notebook_is_colab_ready_and_self_contained():
    nb = load_notebook()
    assert nb["nbformat"] == 4
    assert nb["metadata"]["kernelspec"]["name"] == "python3"
    source = source_text()
    assert "VR2_2021_04_06_1" in source
    assert "54866333" in source and "54183860" in source and "54184214" in source
    assert "from src" not in source and "import reward_encoding" not in source
    assert "N_PER_REGION = 750" in source
    assert "N_PERMUTATIONS = 199" in source
    # The notebook is the source of truth now, so committed outputs would be noise
    # in every diff. Clear them (Edit > Clear all outputs) before committing.
    assert all(cell.get("execution_count") is None for cell in nb["cells"] if cell["cell_type"] == "code")
    assert all(not cell.get("outputs") for cell in nb["cells"] if cell["cell_type"] == "code")


def test_code_cells_compile_and_cell_ids_are_unique():
    nb = load_notebook()
    code_cells = [cell for cell in nb["cells"] if cell["cell_type"] == "code"]
    for index, cell in enumerate(code_cells):
        compile("".join(cell["source"]), f"notebook-cell-{index}", "exec")
    ids = [cell["id"] for cell in nb["cells"]]
    assert len(ids) == len(set(ids))


def test_required_sections_exist():
    source = source_text()
    for heading in [
        "Data download and validation",
        "Balanced neuron sampling",
        "Expanded design matrix",
        "Ridge encoding model",
        "Reward ablation and permutation test",
        "Results and export",
    ]:
        assert heading in source


def test_region_mapping_and_balanced_sampling():
    ns = helper_namespace()
    iarea = np.repeat([8, 0, 5, 3], 300)
    regions = ns["map_regions"](iarea)
    selected, labels = ns["balanced_sample"](regions, 250, seed=42)
    assert len(selected) == 1000
    assert {r: int((labels == r).sum()) for r in np.unique(labels)} == {
        "V1": 250,
        "mHV": 250,
        "lHV": 250,
        "aHV": 250,
    }
    selected_again, _ = ns["balanced_sample"](regions, 250, seed=42)
    assert np.array_equal(selected, selected_again)


def test_event_basis_is_aligned_and_boundary_safe():
    ns = helper_namespace()
    basis = ns["event_basis"](20, np.array([0, 10, 19]), 2.0, -1.0, 1.0, 4)
    assert basis.shape == (20, 4)
    assert np.isfinite(basis).all()
    assert basis[10].sum() > 0


def test_event_basis_skips_events_outside_the_recording():
    ns = helper_namespace()
    basis = ns["event_basis"](20, np.array([-500.0, 500.0]), 2.0, -1.0, 1.0, 4)
    assert basis.shape == (20, 4)
    assert not basis.any()


def test_trial_masks_do_not_leak():
    ns = helper_namespace()
    trials = np.array([1, 1, 2, 2, 3, 3, 4, 4], dtype=float)
    train, test = ns["odd_even_masks"](trials)
    assert not np.any(train & test)
    assert set(trials[train]) == {1, 3}
    assert set(trials[test]) == {2, 4}


def test_metrics_and_corrected_permutation_pvalues():
    ns = helper_namespace()
    y = np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]])
    mse, r2 = ns["regression_metrics"](y, y.copy())
    np.testing.assert_allclose(mse, 0)
    np.testing.assert_allclose(r2, 1)
    observed = np.array([2.0, 0.0])
    null = np.array([[1.0, 1.0], [3.0, -1.0], [0.0, 0.0]])
    np.testing.assert_allclose(ns["permutation_pvalues"](observed, null), [0.5, 0.75])


def test_synthetic_recovery():
    ns = helper_namespace()
    result = ns["run_synthetic_recovery_test"]()
    assert result["injected_delta_mse"] > 0
    assert result["injected_p"] < result["median_null_p"]


def test_align_behavior_frames_trims_small_excess_only():
    ns = helper_namespace()
    beh = {field: np.arange(12.0) for field in ns["FRAME_FIELDS"]}
    aligned = ns["align_behavior_frames"](beh, 10)
    assert all(len(aligned[field]) == 10 for field in ns["FRAME_FIELDS"])
    too_long = {field: np.arange(30.0) for field in ns["FRAME_FIELDS"]}
    with np.testing.assert_raises(ValueError):
        ns["align_behavior_frames"](too_long, 10)


def test_permute_reward_events_actually_breaks_timing():
    """Regression: real reward timing is stereotyped (~10±3 frames into a trial),
    so permuting offsets among trials barely moved events and the null was
    impotent (~53% 'candidates'). The null must re-place each reward at a
    uniform within-trial position instead."""
    ns = helper_namespace()
    rng = np.random.default_rng(0)
    starts = np.arange(100.0) * 100
    ends = starts + 90
    events = starts + 10  # stereotyped timing, as in the real data
    permuted = ns["permute_reward_events"](events, starts, ends, rng)
    assert np.all(permuted >= starts) and np.all(permuted <= ends)
    assert np.std(permuted - starts) > 10  # uniform spread, not the old ±3 shuffle


def test_part_b_uses_reward_ablation_supervised_only():
    """Part B's primary measure is the reward ablation; Part C re-adds the
    cross-validated d'(late vs early cue) as a labelled comparison section.

    The ablation's ablated block is water delivery, defined only for supervised
    mice, and the d' comparison is run on the same supervised sessions for a
    matched comparison, so both stay supervised-only.
    """
    source = source_text()
    # primary ablation pipeline (Part B)
    assert "reward_ablation_session" in source
    assert "N_PERMUTATIONS_OVERTIME" in source
    assert "MIN_DELTA_R2" in source  # effect-size gate; p<0.05 alone flags 50-70%
    # d' comparison section (Part C)
    assert "reward_dprime_session" in source
    assert "DPRIME_THRESHOLD" in source
    # both analyses stay supervised-only: the unsupervised behaviour files never appear
    assert "Beh_unsup" not in source, "d' comparison must stay supervised-only to match Part B"


def test_result_schema_is_stable():
    """The exported CSV keeps the columns downstream analysis reads."""
    source = source_text()
    for column in [
        "neuron_index",
        "region",
        "mse_full",
        "r2_full",
        "mse_reduced",
        "r2_reduced",
        "delta_mse_refit",
        "delta_r2_refit",
        "permutation_p",
        "reward_encoding_candidate",
    ]:
        assert f'"{column}"' in source, f"missing result column: {column}"
