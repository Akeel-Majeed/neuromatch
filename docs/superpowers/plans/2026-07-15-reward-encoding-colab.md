# Reward-Encoding Pilot Colab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a self-contained Colab notebook that downloads Zhong's supervised after-learning session and runs the 1,000-neuron expanded-ridge reward-encoding pilot end to end.

**Architecture:** A deterministic Python builder creates the `.ipynb` from ordered Markdown and code cells so the notebook remains reviewable and reproducible. The generated notebook contains every runtime function and does not import project-local code. Pytest extracts the notebook's tagged helper cells to exercise data-independent behavior, while `nbclient` executes a synthetic mode and then the real-data configuration.

**Tech Stack:** Python 3, Jupyter/nbformat, NumPy, SciPy, pandas, scikit-learn, matplotlib, seaborn, requests, pytest, nbclient.

---

## File structure

- Create `scripts/build_reward_encoding_notebook.py`: deterministic source for Markdown/code cells and notebook metadata.
- Create `src/reward_encoding_pilot_colab.ipynb`: the self-contained browser-ready deliverable produced by the builder.
- Create `tests/test_reward_encoding_notebook.py`: structural, helper, synthetic, and export-schema tests against the generated notebook.
- Modify `README.md`: add a short link and Colab usage note for the new notebook.

### Task 1: Notebook contract and helper tests

**Files:**
- Create: `tests/test_reward_encoding_notebook.py`
- Create: `scripts/build_reward_encoding_notebook.py`

- [ ] **Step 1: Write structural tests before the builder exists**

```python
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "src" / "reward_encoding_pilot_colab.ipynb"

def load_notebook():
    return json.loads(NOTEBOOK.read_text())

def test_notebook_is_colab_ready_and_self_contained():
    nb = load_notebook()
    assert nb["nbformat"] == 4
    assert nb["metadata"]["kernelspec"]["name"] == "python3"
    source = "\n".join("".join(c.get("source", [])) for c in nb["cells"])
    assert "VR2_2021_04_06_1" in source
    assert "54866333" in source and "54183860" in source and "54184214" in source
    assert "from src" not in source and "import reward_encoding" not in source
    assert "N_PER_REGION = 250" in source
    assert "N_PERMUTATIONS = 199" in source

def test_required_sections_exist():
    source = "\n".join("".join(c.get("source", [])) for c in load_notebook()["cells"])
    for heading in [
        "Data download and validation", "Balanced neuron sampling",
        "Expanded design matrix", "Ridge encoding model",
        "Reward ablation and permutation test", "Results and export",
    ]:
        assert heading in source
```

- [ ] **Step 2: Run the tests and verify the expected failure**

Run: `pytest tests/test_reward_encoding_notebook.py -v`

Expected: FAIL because `src/reward_encoding_pilot_colab.ipynb` does not exist.

- [ ] **Step 3: Add a deterministic builder skeleton**

```python
#!/usr/bin/env python3
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "src" / "reward_encoding_pilot_colab.ipynb"

def md(text, tags=()):
    cell = nbf.v4.new_markdown_cell(text.strip() + "\n")
    cell.metadata["tags"] = list(tags)
    return cell

def code(text, tags=()):
    cell = nbf.v4.new_code_cell(text.strip() + "\n")
    cell.metadata["tags"] = list(tags)
    return cell

def build_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "colab": {"name": "Reward encoding pilot — Zhong et al. 2025", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    }
    nb.cells = [md("# Reward-encoding pilot: Zhong et al. 2025")]
    return nb

if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(build_notebook(), OUTPUT)
    print(OUTPUT)
```

- [ ] **Step 4: Generate the skeleton and confirm only content assertions fail**

Run: `python3 scripts/build_reward_encoding_notebook.py && pytest tests/test_reward_encoding_notebook.py -v`

Expected: notebook JSON loads; tests fail on missing session/configuration/section content.

- [ ] **Step 5: Commit the contract**

```bash
git add scripts/build_reward_encoding_notebook.py src/reward_encoding_pilot_colab.ipynb tests/test_reward_encoding_notebook.py
git commit -m "test: define reward encoding notebook contract"
```

### Task 2: Data loading, validation, sampling, and feature construction

**Files:**
- Modify: `scripts/build_reward_encoding_notebook.py`
- Regenerate: `src/reward_encoding_pilot_colab.ipynb`
- Modify: `tests/test_reward_encoding_notebook.py`

- [ ] **Step 1: Add helper-cell extraction and focused unit tests**

```python
import numpy as np

def helper_namespace():
    nb = load_notebook()
    ns = {}
    for cell in nb["cells"]:
        if "unit-testable" in cell.get("metadata", {}).get("tags", []):
            exec("".join(cell["source"]), ns)
    return ns

def test_region_mapping_and_balanced_sampling():
    ns = helper_namespace()
    iarea = np.repeat([8, 0, 5, 3], 300)
    regions = ns["map_regions"](iarea)
    selected, labels = ns["balanced_sample"](regions, 250, seed=42)
    assert len(selected) == 1000
    assert {r: int((labels == r).sum()) for r in np.unique(labels)} == {
        "V1": 250, "mHV": 250, "lHV": 250, "aHV": 250,
    }
    assert np.array_equal(selected, ns["balanced_sample"](regions, 250, seed=42)[0])

def test_event_basis_is_aligned_and_boundary_safe():
    ns = helper_namespace()
    basis = ns["event_basis"](20, np.array([0, 10, 19]), 2.0, -1.0, 1.0, 4)
    assert basis.shape == (20, 4)
    assert np.isfinite(basis).all()
    assert basis[10].sum() > 0

def test_trial_masks_do_not_leak():
    ns = helper_namespace()
    trials = np.array([1, 1, 2, 2, 3, 3, 4, 4], dtype=float)
    train, test = ns["odd_even_masks"](trials)
    assert not np.any(train & test)
    assert set(trials[train]) == {1, 3}
    assert set(trials[test]) == {2, 4}
```

- [ ] **Step 2: Run the focused tests and verify helper names are missing**

Run: `pytest tests/test_reward_encoding_notebook.py -k 'region or event or trial' -v`

Expected: FAIL with missing `map_regions`, `balanced_sample`, `event_basis`, and `odd_even_masks`.

- [ ] **Step 3: Implement the notebook's configuration and download layer**

Add cells defining the exact runtime constants and a safe downloader:

```python
SESSION = "VR2_2021_04_06_1"
SEED = 42
N_PER_REGION = 250
N_PERMUTATIONS = 199
DATA_DIR = Path("/content/Zhong_et_al_2025")
FILES = {
    "behavior": (54183860, "Beh_sup_train1_after_learning.npy"),
    "svd": (54866333, "VR2_2021_04_06_1_SVD_dec.npy"),
    "retinotopy": (54184214, "VR2_2021_04_06_trans.npz"),
}

def download_figshare_file(file_id, filename, data_dir=DATA_DIR):
    data_dir.mkdir(parents=True, exist_ok=True)
    target, partial = data_dir / filename, data_dir / f"{filename}.part"
    if target.exists() and target.stat().st_size > 0:
        return target
    with requests.get(f"https://ndownloader.figshare.com/files/{file_id}", stream=True, timeout=(15, 180)) as response:
        response.raise_for_status()
        with partial.open("wb") as handle:
            for chunk in response.iter_content(1024 * 1024):
                if chunk:
                    handle.write(chunk)
    if partial.stat().st_size == 0:
        raise RuntimeError(f"Figshare returned an empty file for {filename}")
    partial.replace(target)
    return target
```

- [ ] **Step 4: Implement validation, region mapping, balanced sampling, and selected-neuron reconstruction**

```python
AREA_CODES = {"V1": (8,), "mHV": (0, 1, 2, 9), "lHV": (5, 6), "aHV": (3, 4)}

def map_regions(iarea):
    labels = np.full(len(iarea), "unmapped", dtype=object)
    for name, codes in AREA_CODES.items():
        labels[np.isin(iarea, codes)] = name
    return labels.astype(str)

def balanced_sample(regions, n_per_region, seed=42):
    rng, chunks, labels = np.random.default_rng(seed), [], []
    for region in AREA_CODES:
        candidates = np.flatnonzero(regions == region)
        if len(candidates) < n_per_region:
            raise ValueError(f"{region} has {len(candidates)} neurons; need {n_per_region}")
        chosen = np.sort(rng.choice(candidates, n_per_region, replace=False))
        chunks.append(chosen)
        labels.extend([region] * n_per_region)
    return np.concatenate(chunks), np.asarray(labels)

def reconstruct_selected(svd, selected):
    U, V = np.asarray(svd["U"]), np.asarray(svd["V"])
    if U.shape[1] <= selected.max():
        raise ValueError("Selected neuron index exceeds SVD U neuron axis")
    return (U[:, selected].T @ V).T.astype(np.float32, copy=False)
```

- [ ] **Step 5: Implement raised-cosine bases, event expansion, split validation, and the block manifest**

Use a single `DesignMatrix` dataclass containing `raw`, `names`, and `blocks`. `build_design_matrix(beh)` must create stimulus, 12-position, position×stimulus, speed, movement, acceleration, eight reward, eight lick, eight cue, four epoch, and eighteen landmark columns with the windows fixed in the design spec. `event_basis` clips kernels at recording boundaries and ignores NaN/out-of-range event indices. `odd_even_masks` derives split membership from integer-valued finite `ft_trInd` and raises if either split is empty.

```python
@dataclass
class DesignMatrix:
    raw: np.ndarray
    names: list[str]
    blocks: dict[str, np.ndarray]

def odd_even_masks(frame_trials):
    valid = np.isfinite(frame_trials)
    rounded = np.rint(frame_trials[valid])
    if not np.allclose(frame_trials[valid], rounded):
        raise ValueError("ft_trInd contains non-integer trial IDs")
    train = valid & (np.rint(frame_trials).astype(np.int64) % 2 == 1)
    test = valid & (np.rint(frame_trials).astype(np.int64) % 2 == 0)
    if not train.any() or not test.any() or np.any(train & test):
        raise ValueError("Odd/even trial split is invalid")
    return train, test
```

- [ ] **Step 6: Regenerate and run unit tests**

Run: `python3 scripts/build_reward_encoding_notebook.py && pytest tests/test_reward_encoding_notebook.py -v`

Expected: all structural and helper tests for Task 2 PASS.

- [ ] **Step 7: Commit the data and design-matrix layer**

```bash
git add scripts/build_reward_encoding_notebook.py src/reward_encoding_pilot_colab.ipynb tests/test_reward_encoding_notebook.py
git commit -m "feat: add Zhong data and design matrix pipeline"
```

### Task 3: Ridge fitting, ablations, permutation inference, and exports

**Files:**
- Modify: `scripts/build_reward_encoding_notebook.py`
- Regenerate: `src/reward_encoding_pilot_colab.ipynb`
- Modify: `tests/test_reward_encoding_notebook.py`

- [ ] **Step 1: Add metric, transformation, and p-value tests**

```python
def test_metrics_and_corrected_permutation_pvalues():
    ns = helper_namespace()
    y = np.array([[0., 1.], [1., 2.], [2., 3.]])
    mse, r2 = ns["regression_metrics"](y, y.copy())
    np.testing.assert_allclose(mse, 0)
    np.testing.assert_allclose(r2, 1)
    observed = np.array([2., 0.])
    null = np.array([[1., 1.], [3., -1.], [0., 0.]])
    np.testing.assert_allclose(ns["permutation_pvalues"](observed, null), [0.5, 0.5])

def test_zero_out_uses_transformed_reward_absence():
    ns = helper_namespace()
    X = np.array([[0., 1.], [0., 2.], [1., 3.], [1., 4.]])
    transformer = ns["fit_transformer"](X[:3], {"reward": np.array([0])})
    transformed = ns["apply_transformer"](X, transformer)
    zeroed = ns["zero_reward_block"](transformed, transformer)
    expected_absent = ns["apply_transformer"](np.array([[0., 1.]]), transformer)[0, 0]
    np.testing.assert_allclose(zeroed[:, 0], expected_absent)
```

- [ ] **Step 2: Run the new tests and verify expected missing-function failures**

Run: `pytest tests/test_reward_encoding_notebook.py -k 'metric or zero_out' -v`

Expected: FAIL with missing modeling helper functions.

- [ ] **Step 3: Implement training-only transformation and grouped alpha selection**

`fit_transformer` records kept columns, means, scales, binary flags, transformed block indices, and the transformed reward-absent vector. `select_alpha` evaluates `[0.01, 0.1, 1, 10, 100, 1000]` with three `GroupKFold` splits over odd trial IDs and returns the alpha with minimum mean neuron-averaged validation MSE. All ridge fits use `fit_intercept=True` and multi-target `Y`.

```python
def regression_metrics(y_true, y_pred):
    residual = np.mean((y_true - y_pred) ** 2, axis=0)
    denom = np.sum((y_true - y_true.mean(axis=0)) ** 2, axis=0)
    numer = np.sum((y_true - y_pred) ** 2, axis=0)
    r2 = np.where(denom > 0, 1.0 - numer / denom, np.nan)
    return residual, r2

def fit_ridge(X, Y, alpha):
    return Ridge(alpha=float(alpha), fit_intercept=True).fit(X, Y)
```

- [ ] **Step 4: Implement full, zero-out, and reduced fits**

Fit the full model on odd rows, predict even rows, then replace the reward columns with their transformed raw-zero values for the zero-out prediction. Fit the reduced model on matrices with transformed reward indices removed. Return full/zero/reduced MSE and R², `delta_mse_zero`, `delta_mse_refit`, `delta_r2_refit`, and full-model reward coefficients.

- [ ] **Step 5: Implement deterministic reward-timing permutations for all neurons**

Map each finite `RewardFr` event to its trial ID. For each permutation, permute event offsets relative to trial starts among reward-bearing trials, rebuild the raw reward basis while keeping all other columns fixed, apply the original training transformer, refit the full model at the selected alpha, and calculate the refit-style held-out ΔMSE against the fixed reduced-model MSE. Store a `(199, 1000)` float32 null matrix and calculate:

```python
def permutation_pvalues(observed, null):
    observed = np.asarray(observed)[None, :]
    null = np.asarray(null)
    return (1 + np.sum(null >= observed, axis=0)) / (null.shape[0] + 1)
```

Candidate status is `(delta_mse_refit > 0) & (p_value < 0.05)` with no screening restriction.

- [ ] **Step 6: Add figures and exports**

Create data-QC tables, block manifest, alpha-CV curve, held-out metric histograms, zero-out/refit scatter, representative null distributions, representative reward coefficients, and region summary with Wilson 95% intervals. Export `reward_encoding_pilot_results.csv` and `reward_encoding_pilot_run_manifest.json` under `/content`, assert their schemas after writing, and offer `google.colab.files.download` only when running in Colab.

- [ ] **Step 7: Add a synthetic recovery cell and tests**

The tagged synthetic cell builds grouped trials, nuisance features, an event reward block, one injected reward target, and null targets. It must assert the injected target has positive refit ΔMSE and a smaller permutation p-value than the median null p-value. Add a pytest that executes this tagged cell after helper cells.

- [ ] **Step 8: Regenerate and run all data-independent tests**

Run: `python3 scripts/build_reward_encoding_notebook.py && pytest tests/test_reward_encoding_notebook.py -v`

Expected: all tests PASS.

- [ ] **Step 9: Commit the completed analysis notebook**

```bash
git add scripts/build_reward_encoding_notebook.py src/reward_encoding_pilot_colab.ipynb tests/test_reward_encoding_notebook.py
git commit -m "feat: add reward encoding ridge analysis"
```

### Task 4: Browser guidance and end-to-end verification

**Files:**
- Modify: `README.md`
- Modify if verification exposes defects: `scripts/build_reward_encoding_notebook.py`
- Regenerate if changed: `src/reward_encoding_pilot_colab.ipynb`
- Modify if needed: `tests/test_reward_encoding_notebook.py`

- [ ] **Step 1: Add the notebook link and usage instructions**

Add a README section that links `src/reward_encoding_pilot_colab.ipynb`, tells the user to upload/open it in Colab and choose **Runtime → Run all**, states the default download size/runtime configuration, and names the generated CSV/JSON outputs.

- [ ] **Step 2: Validate deterministic generation and notebook syntax**

Run:

```bash
python3 scripts/build_reward_encoding_notebook.py
cp src/reward_encoding_pilot_colab.ipynb /tmp/reward_encoding_pilot_colab.ipynb
python3 scripts/build_reward_encoding_notebook.py
cmp /tmp/reward_encoding_pilot_colab.ipynb src/reward_encoding_pilot_colab.ipynb
python3 -m json.tool src/reward_encoding_pilot_colab.ipynb >/dev/null
```

Expected: `cmp` exits 0 and JSON validation succeeds.

- [ ] **Step 3: Execute the synthetic notebook path cleanly**

Run: `pytest tests/test_reward_encoding_notebook.py -v`

Expected: all structural, unit, and synthetic recovery tests PASS.

- [ ] **Step 4: Execute the real-data notebook end to end**

Run the notebook with `nbclient` from a fresh working directory using the default `N_PER_REGION=250` and `N_PERMUTATIONS=199`, allowing sufficient cell timeout for downloads and permutations. Capture elapsed time and maximum resident memory. Expected: every cell succeeds; the notebook prints 1,000 selected neurons, nonempty odd/even splits, full/reduced metrics, and a region summary; both export files exist and parse successfully.

- [ ] **Step 5: Re-run verification after any fixes**

Run:

```bash
python3 scripts/build_reward_encoding_notebook.py
pytest tests/test_reward_encoding_notebook.py -v
git diff --check
git status --short
```

Expected: all tests PASS, no whitespace errors, and only intended files are modified.

- [ ] **Step 6: Commit documentation and verified fixes**

```bash
git add README.md scripts/build_reward_encoding_notebook.py src/reward_encoding_pilot_colab.ipynb tests/test_reward_encoding_notebook.py
git commit -m "docs: add verified Colab reward encoding workflow"
```
