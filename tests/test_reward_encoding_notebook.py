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
    assert "from src" not in source and "import reward_encoding" not in source
    assert "DPRIME_THRESHOLD = 0.3" in source
    assert "N_PER_REGION = 250" in source
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
        "Data access",
        "Region mapping and balanced neuron sampling",
        "Cross-validated d′(late vs early cue)",
        "Run across cohorts, stages, and animals",
        "Results — proportion and activation across learning, by region and cohort",
        "Interpretation checklist",
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


def test_reconstruct_selected_shape():
    ns = helper_namespace()
    rng = np.random.default_rng(0)
    svd = {"U": rng.standard_normal((5, 10)).astype("float32"),
           "V": rng.standard_normal((5, 20)).astype("float32")}
    activity = ns["reconstruct_selected"](svd, [0, 2, 4])
    assert activity.shape == (20, 3)  # frames x selected neurons


def test_dprime_synthetic_recovery():
    """One ramping neuron among noise; the cross-validated flag must catch the
    ramp and nothing else — the same self-check the notebook runs live."""
    ns = helper_namespace()
    result = ns["run_dprime_synthetic_check"]()
    assert result["flagged"] == 1
    assert result["ramp_strength"] >= ns["DPRIME_THRESHOLD"]


def test_reward_encoding_is_cross_validated_not_single_shot():
    """Regression: a single |d'|>=threshold on all trials is noisy with few
    trials; both interleaved folds must agree in magnitude AND sign, or the
    neuron must not be flagged even if each fold alone looks like a hit."""
    ns = helper_namespace()
    rng = np.random.default_rng(1)
    late = np.array([False] * 20 + [True] * 20)  # pre-sorted -> argsort is identity
    fold_a = np.arange(40) % 2 == 0
    tm = rng.normal(0, 0.3, (1, 40)).astype(np.float32)
    tm[0, fold_a & late] += 3.0     # fold A: late higher -> large positive d'
    tm[0, fold_a & ~late] -= 3.0
    tm[0, ~fold_a & late] -= 3.0    # fold B: late lower -> large negative d' (sign flip)
    tm[0, ~fold_a & ~late] += 3.0
    flag, strength = ns["_reward_encoding"](tm, late, ns["DPRIME_THRESHOLD"])
    assert not flag[0], "opposite-sign folds must not be flagged as reward-encoding"
    assert strength[0] > ns["DPRIME_THRESHOLD"]  # each fold alone would clear the bar


def test_both_cohorts_present_for_a_fair_comparison():
    """d'(late vs early cue) doesn't depend on reward, unlike the retired
    ablation (which needed water and so was supervised-only). Both cohorts
    should be scored on the same index for a fair comparison."""
    source = source_text()
    assert "Beh_sup_train1_before_learning.npy" in source
    assert "Beh_unsup_train1_before_learning.npy" in source
    assert '"supervised"' in source and '"unsupervised"' in source


def test_animal_pairing_uses_short_id_not_session_key():
    """Before/after are different recording sessions (different dates) for the
    same animal, so pairing must key on the short animal id, not the full
    session string."""
    source = source_text()
    assert 'animal_id(session_key)' in source
    assert 'session_key.split("_")[0]' in source


def test_result_schema_is_stable():
    """The exported CSV keeps the columns downstream analysis reads."""
    source = source_text()
    for column in [
        "cohort",
        "stage",
        "region",
        "animal",
        "mouse",
        "pct_reward",
        "mean_dprime",
        "n_neurons",
    ]:
        assert f'"{column}"' in source, f"missing result column: {column}"
