#!/usr/bin/env python3
"""Build the self-contained reward-encoding Colab notebook."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "src" / "reward_encoding_pilot_colab.ipynb"


def md(text: str, tags=()):
    cell = nbf.v4.new_markdown_cell(dedent(text).strip() + "\n")
    cell.metadata["tags"] = list(tags)
    return cell


def code(text: str, tags=()):
    cell = nbf.v4.new_code_cell(dedent(text).strip() + "\n")
    cell.metadata["tags"] = list(tags)
    return cell


def build_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "colab": {
            "name": "Reward encoding pilot — Zhong et al. 2025",
            "provenance": [],
            "toc_visible": True,
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
    }

    nb.cells = [
        md(
            r"""
            # Reward-encoding pilot: Zhong et al. 2025

            This notebook is a **one-mouse, one-session feasibility test** of the Neuromatch
            proposal. It downloads Zhong et al.'s supervised after-learning session, selects
            1,000 neurons balanced across four visual-cortical regions, builds the expanded
            design matrix, fits per-neuron ridge encoding models, and asks whether removing
            reward timing worsens held-out prediction.

            **Run in Colab:** choose **Runtime → Run all**. No Drive mount or manual data upload
            is required. The default downloads are about 258 MB. The final CSV and JSON files
            are written to `/content` and offered for download when Colab is detected.

            Important interpretation: neurons are not independent biological replicates. Raw
            `p < 0.05` is used because that was the selected pilot rule, but with 1,000 tests
            false positives are expected. Region percentages here are descriptive, not
            animal-level or longitudinal evidence.
            """
        ),
        md(
            """
            ## 1. Setup and configuration

            Colab already includes the scientific Python packages used below. The configuration
            cell is the only place to change sample size, permutation count, or random seed.
            """
        ),
        code(
            r"""
            from __future__ import annotations

            import json
            import math
            import os
            import platform
            import sys
            import time
            import warnings
            from dataclasses import asdict, dataclass
            from pathlib import Path

            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            import requests
            import seaborn as sns
            import sklearn
            from scipy import linalg
            from sklearn.model_selection import GroupKFold

            sns.set_theme(style="whitegrid", context="notebook")
            np.set_printoptions(precision=4, suppress=True)
            """,
            tags=("unit-testable",),
        ),
        code(
            r"""
            SESSION = "VR2_2021_04_06_1"
            SEED = 42
            N_PER_REGION = 250
            N_PERMUTATIONS = 199
            ALPHAS = np.array([0.01, 0.1, 1.0, 10.0, 100.0, 1000.0])
            DATA_DIR = Path("/content/Zhong_et_al_2025")
            OUTPUT_DIR = Path("/content")

            # Figshare file id, exact filename, and expected byte count.
            FILES = {
                "behavior": (54183860, "Beh_sup_train1_after_learning.npy", 113_352_887),
                "svd": (54866333, "VR2_2021_04_06_1_SVD_dec.npy", 142_132_066),
                "retinotopy": (54184214, "VR2_2021_04_06_trans.npz", 2_559_726),
            }

            RESULT_COLUMNS = [
                "neuron_index", "region", "mse_full", "r2_full", "mse_reduced",
                "r2_reduced", "delta_mse_zero", "delta_mse_refit",
                "delta_r2_refit", "permutation_p", "reward_encoding_candidate",
            ]

            print(f"Python {platform.python_version()} | NumPy {np.__version__} | "
                  f"scikit-learn {sklearn.__version__}")
            print(f"Seed={SEED}, neurons={4 * N_PER_REGION}, permutations={N_PERMUTATIONS}")
            """,
            tags=("unit-testable",),
        ),
        md(
            """
            ## 2. Data download and validation

            Files are streamed from the official Figshare deposit, checked against their known
            byte counts, and atomically renamed only after a complete download. Zhong's SVD file
            contains an unused serialized scikit-learn object; this notebook reads only `U` and
            `V` from that trusted official file.
            """
        ),
        code(
            r"""
            AREA_CODES = {
                "V1": (8,),
                "mHV": (0, 1, 2, 9),
                "lHV": (5, 6),
                "aHV": (3, 4),
            }

            FRAME_FIELDS = (
                "ft", "ft_trInd", "ft_trInd_odd", "ft_trInd_even", "ft_WallID",
                "ft_Pos", "ft_RunSpeed", "ft_isMoving", "ft_move", "BefCueFr",
                "AftCueFr", "ft_GraySpc", "ft_CorrSpc",
            )


            @dataclass
            class DesignMatrix:
                raw: np.ndarray
                names: list[str]
                blocks: dict[str, np.ndarray]
                frame_rate: float


            @dataclass
            class Transformer:
                keep_indices: np.ndarray
                mean: np.ndarray
                scale: np.ndarray
                blocks: dict[str, np.ndarray]
                block_source_positions: dict[str, np.ndarray]
                reward_indices: np.ndarray
                reward_absent: np.ndarray
                names: list[str]


            @dataclass
            class RidgeFit:
                coef: np.ndarray  # features × targets
                intercept: np.ndarray  # targets
                alpha: float

                def predict(self, X):
                    return np.asarray(X) @ self.coef + self.intercept


            @dataclass
            class ModelResults:
                full_fit: RidgeFit
                reduced_fit: RidgeFit
                reduced_indices: np.ndarray
                mse_full: np.ndarray
                r2_full: np.ndarray
                mse_zero: np.ndarray
                r2_zero: np.ndarray
                mse_reduced: np.ndarray
                r2_reduced: np.ndarray
                delta_mse_zero: np.ndarray
                delta_mse_refit: np.ndarray
                delta_r2_refit: np.ndarray


            def download_figshare_file(file_id, filename, expected_size, data_dir=DATA_DIR):
                data_dir = Path(data_dir)
                data_dir.mkdir(parents=True, exist_ok=True)
                target = data_dir / filename
                partial = data_dir / f"{filename}.part"
                if target.exists():
                    if target.stat().st_size == expected_size:
                        print(f"Using cached {filename} ({expected_size / 1e6:.1f} MB)")
                        return target
                    print(f"Removing incomplete cached file: {filename}")
                    target.unlink()
                partial.unlink(missing_ok=True)
                url = f"https://ndownloader.figshare.com/files/{file_id}"
                print(f"Downloading {filename} ({expected_size / 1e6:.1f} MB) …")
                try:
                    with requests.get(
                        url,
                        stream=True,
                        timeout=(15, 180),
                        headers={"User-Agent": "Neuromatch-reward-encoding-pilot/1.0"},
                    ) as response:
                        response.raise_for_status()
                        with partial.open("wb") as handle:
                            for chunk in response.iter_content(1024 * 1024):
                                if chunk:
                                    handle.write(chunk)
                    actual = partial.stat().st_size
                    if actual != expected_size:
                        raise RuntimeError(
                            f"Incomplete download for {filename}: expected {expected_size} bytes, got {actual}. "
                            "Delete the .part file and rerun this cell."
                        )
                    partial.replace(target)
                except Exception:
                    partial.unlink(missing_ok=True)
                    raise
                return target


            def align_behavior_frames(beh, n_frames):
                '''Return a shallow copy whose frame-aligned arrays match neural frames.'''
                aligned = dict(beh)
                notes = []
                for field in FRAME_FIELDS:
                    if field not in beh:
                        raise KeyError(f"Required behavior field is missing: {field}")
                    values = np.asarray(beh[field])
                    if len(values) == n_frames:
                        aligned[field] = values
                    elif len(values) == n_frames + 1:
                        # The official session has one terminal behavior sample without an SVD frame.
                        aligned[field] = values[:n_frames]
                        notes.append(field)
                    else:
                        raise ValueError(
                            f"{field} has {len(values)} frames but neural data has {n_frames}; "
                            "expected an exact match or the dataset's documented single terminal sample."
                        )
                if notes:
                    print(
                        f"Validated official one-sample terminal offset; removed the final behavior-only "
                        f"sample from {len(notes)} frame-aligned fields."
                    )
                return aligned


            def infer_frame_rate(ft):
                ft = np.asarray(ft, dtype=float)
                diffs = np.diff(ft[np.isfinite(ft)])
                diffs = diffs[diffs > 0]
                if not len(diffs):
                    raise ValueError("Cannot infer frame rate from beh['ft']")
                dt = float(np.median(diffs))
                # Zhong timestamps are MATLAB datenums (days); ordinary second timestamps also work.
                dt_seconds = dt * 86400.0 if dt < 0.01 else dt
                if not 0.01 <= dt_seconds <= 10.0:
                    raise ValueError(f"Implausible neural frame interval: {dt_seconds:.6g} seconds")
                return 1.0 / dt_seconds


            def map_regions(iarea):
                iarea = np.asarray(iarea)
                labels = np.full(len(iarea), "unmapped", dtype=object)
                for name, codes in AREA_CODES.items():
                    labels[np.isin(iarea, codes)] = name
                return labels.astype(str)


            def balanced_sample(regions, n_per_region, seed=42):
                regions = np.asarray(regions)
                rng = np.random.default_rng(seed)
                selected, labels = [], []
                for region in AREA_CODES:
                    candidates = np.flatnonzero(regions == region)
                    if len(candidates) < n_per_region:
                        raise ValueError(
                            f"{region} has {len(candidates)} mapped neurons; need {n_per_region}."
                        )
                    chosen = np.sort(rng.choice(candidates, n_per_region, replace=False))
                    selected.append(chosen)
                    labels.extend([region] * n_per_region)
                return np.concatenate(selected), np.asarray(labels)


            def reconstruct_selected(svd, selected):
                if not {"U", "V"}.issubset(svd):
                    raise KeyError("SVD file must contain U and V")
                U = np.asarray(svd["U"], dtype=np.float32)
                V = np.asarray(svd["V"], dtype=np.float32)
                selected = np.asarray(selected, dtype=int)
                if U.ndim != 2 or V.ndim != 2 or U.shape[0] != V.shape[0]:
                    raise ValueError(f"Incompatible SVD shapes: U={U.shape}, V={V.shape}")
                if selected.min() < 0 or selected.max() >= U.shape[1]:
                    raise IndexError("Selected neuron index is outside the SVD U neuron axis")
                # U is components × neurons; V is components × frames.
                return (U[:, selected].T @ V).T.astype(np.float32, copy=False)
            """,
            tags=("unit-testable",),
        ),
        code(
            r"""
            def raised_cosine_basis(values, low, high, n_basis):
                values = np.asarray(values, dtype=float)
                if not np.isfinite(low) or not np.isfinite(high) or high <= low:
                    raise ValueError(f"Invalid raised-cosine range: {low}, {high}")
                centers = np.linspace(low, high, n_basis)
                spacing = (high - low) / max(n_basis - 1, 1)
                width = max(spacing * 1.5, np.finfo(float).eps)
                distance = (values[:, None] - centers[None, :]) / width
                basis = np.zeros((len(values), n_basis), dtype=np.float32)
                inside = np.isfinite(distance) & (np.abs(distance) <= 1)
                basis[inside] = (0.5 + 0.5 * np.cos(np.pi * distance[inside])).astype(np.float32)
                return basis


            def event_basis(n_frames, events, frame_rate, start_s, end_s, n_basis):
                '''Expand fractional frame events into raised-cosine lag columns.'''
                if n_frames <= 0 or frame_rate <= 0 or end_s <= start_s or n_basis <= 0:
                    raise ValueError("Invalid event-basis dimensions or time window")
                output = np.zeros((int(n_frames), int(n_basis)), dtype=np.float32)
                events = np.asarray(events, dtype=float).ravel()
                events = events[np.isfinite(events)]
                centers = np.linspace(start_s, end_s, n_basis)
                spacing = (end_s - start_s) / max(n_basis - 1, 1)
                width = max(spacing * 1.5, np.finfo(float).eps)
                for event in events:
                    if event < -end_s * frame_rate or event > (n_frames - 1) - start_s * frame_rate:
                        continue
                    first = max(0, int(math.floor(event + start_s * frame_rate)))
                    last = min(n_frames - 1, int(math.ceil(event + end_s * frame_rate)))
                    frames = np.arange(first, last + 1)
                    lags = (frames - event) / frame_rate
                    distance = (lags[:, None] - centers[None, :]) / width
                    inside = np.abs(distance) <= 1
                    values = np.zeros_like(distance, dtype=np.float32)
                    values[inside] = (0.5 + 0.5 * np.cos(np.pi * distance[inside])).astype(np.float32)
                    output[frames] += values
                return output


            def odd_even_masks(frame_trials):
                '''Use first/third/etc. trials for train, matching Zhong's supplied 'odd' mask.'''
                frame_trials = np.asarray(frame_trials, dtype=float)
                valid = np.isfinite(frame_trials)
                rounded = np.rint(frame_trials[valid])
                if not np.allclose(frame_trials[valid], rounded):
                    raise ValueError("ft_trInd contains non-integer trial IDs")
                trial_ids = np.unique(rounded.astype(np.int64))
                if len(trial_ids) < 2:
                    raise ValueError("At least two trials are required")
                train_ids, test_ids = trial_ids[::2], trial_ids[1::2]
                train = valid & np.isin(np.rint(frame_trials), train_ids)
                test = valid & np.isin(np.rint(frame_trials), test_ids)
                if not train.any() or not test.any() or np.any(train & test):
                    raise ValueError("Odd/even trial split is empty or overlapping")
                return train, test


            def _append_block(arrays, names, blocks, block_name, values, column_names):
                values = np.asarray(values, dtype=np.float32)
                if values.ndim == 1:
                    values = values[:, None]
                if values.shape[1] != len(column_names):
                    raise ValueError(f"Name count mismatch in block {block_name}")
                start = sum(array.shape[1] for array in arrays)
                arrays.append(values)
                names.extend(column_names)
                blocks[block_name] = np.arange(start, start + values.shape[1], dtype=int)


            def build_design_matrix(beh, train_mask, reward_events=None):
                required = [
                    "ft", "ft_WallID", "ft_Pos", "ft_RunSpeed", "ft_isMoving",
                    "ft_trInd", "LickFr", "RewardFr", "BefCueFr", "AftCueFr",
                    "ft_GraySpc", "ft_CorrSpc", "StartFr", "GrayFr", "EndFr",
                ]
                missing = [field for field in required if field not in beh]
                if missing:
                    raise KeyError(f"Missing behavior fields: {missing}")
                n_frames = len(np.asarray(beh["ft"]))
                train_mask = np.asarray(train_mask, dtype=bool)
                if len(train_mask) != n_frames or not train_mask.any():
                    raise ValueError("train_mask must align to frames and contain training rows")
                frame_rate = infer_frame_rate(beh["ft"])
                arrays, names, blocks = [], [], {}

                wall = np.asarray(beh["ft_WallID"]).astype(str)
                stimuli = sorted(value for value in np.unique(wall) if value.lower() != "nan")
                if len(stimuli) < 2:
                    raise ValueError(f"Expected at least two stimuli, found {stimuli}")
                stimulus = np.column_stack([wall == value for value in stimuli]).astype(np.float32)
                _append_block(arrays, names, blocks, "stimulus", stimulus,
                              [f"stimulus:{value}" for value in stimuli])

                position = np.asarray(beh["ft_Pos"], dtype=float)
                position_basis = raised_cosine_basis(position, 0.0, 60.0, 12)
                _append_block(arrays, names, blocks, "position", position_basis,
                              [f"position_basis:{i}" for i in range(12)])
                interactions = (stimulus[:, :, None] * position_basis[:, None, :]).reshape(n_frames, -1)
                _append_block(
                    arrays, names, blocks, "position_x_stimulus", interactions,
                    [f"position_x_stimulus:{stim}:{i}" for stim in stimuli for i in range(12)],
                )

                speed = np.asarray(beh["ft_RunSpeed"], dtype=float)
                finite_train_speed = speed[train_mask & np.isfinite(speed)]
                if not len(finite_train_speed):
                    raise ValueError("No finite training running-speed values")
                speed_fill = float(np.median(finite_train_speed))
                speed = np.where(np.isfinite(speed), speed, speed_fill)
                low, high = np.percentile(finite_train_speed, [1, 99])
                if high <= low:
                    high = low + 1.0
                speed_basis = raised_cosine_basis(speed, float(low), float(high), 5)
                movement_values = np.column_stack([
                    speed,
                    speed_basis,
                    np.asarray(beh["ft_isMoving"], dtype=np.float32),
                    np.diff(speed, prepend=speed[0]),
                ])
                _append_block(
                    arrays, names, blocks, "movement", movement_values,
                    ["running_speed"] + [f"speed_basis:{i}" for i in range(5)]
                    + ["is_moving", "acceleration"],
                )

                if reward_events is None:
                    reward_events = np.asarray(beh["RewardFr"], dtype=float)
                reward = event_basis(n_frames, reward_events, frame_rate, -3.0, 3.0, 8)
                _append_block(arrays, names, blocks, "reward", reward,
                              [f"reward_lag_basis:{i}" for i in range(8)])

                lick = event_basis(n_frames, beh["LickFr"], frame_rate, -1.0, 2.0, 8)
                _append_block(arrays, names, blocks, "lick", lick,
                              [f"lick_lag_basis:{i}" for i in range(8)])

                cue_field = "SoundDelayFr" if "SoundDelayFr" in beh else "SoundFr"
                if cue_field not in beh:
                    raise KeyError("Neither SoundDelayFr nor SoundFr is available")
                cue = event_basis(n_frames, beh[cue_field], frame_rate, 0.0, 3.0, 8)
                _append_block(arrays, names, blocks, "cue", cue,
                              [f"cue_lag_basis:{i}" for i in range(8)])

                epoch = np.column_stack([
                    beh["BefCueFr"], beh["AftCueFr"], beh["ft_GraySpc"], beh["ft_CorrSpc"],
                ]).astype(np.float32)
                _append_block(arrays, names, blocks, "epoch", epoch,
                              ["before_cue", "after_cue", "gray_space", "corridor_space"])

                for source, label in [("StartFr", "start"), ("GrayFr", "gray"), ("EndFr", "end")]:
                    landmark = event_basis(n_frames, beh[source], frame_rate, 0.0, 2.0, 6)
                    _append_block(arrays, names, blocks, f"landmark_{label}", landmark,
                                  [f"landmark_{label}_basis:{i}" for i in range(6)])

                raw = np.column_stack(arrays).astype(np.float32, copy=False)
                if not np.isfinite(raw).all():
                    bad = np.flatnonzero(~np.isfinite(raw).all(axis=0))
                    raise ValueError(f"Design matrix has non-finite columns: {bad[:10].tolist()}")
                return DesignMatrix(raw=raw, names=names, blocks=blocks, frame_rate=frame_rate)
            """,
            tags=("unit-testable",),
        ),
        md(
            """
            ## 3. Balanced neuron sampling

            Region membership comes from the retinotopy file. We sample exactly 250 neurons from
            each mapped region with a fixed seed, independently of activity or model fit, then
            reconstruct only those neurons from Zhong's 400-component SVD representation.
            """
        ),
        md(
            """
            ## 4. Expanded design matrix

            The matrix follows `design-matrix-flowchart.pdf`: stimulus identity; 12 position
            bases; position×stimulus interactions; speed, speed bases, movement and acceleration;
            reward, lick and cue lag bases; cue/space epochs; and corridor landmarks. Reward bases
            span −3 to +3 seconds to cover anticipation and delivery. An unpenalized intercept is
            fitted separately by the ridge solver. Continuous columns are centered/scaled using
            training frames only; binary columns remain 0/1.
            """
        ),
        code(
            r"""
            def fit_transformer(X_train, blocks, names=None):
                X_train = np.asarray(X_train, dtype=float)
                if X_train.ndim != 2 or not np.isfinite(X_train).all():
                    raise ValueError("Training design matrix must be finite and two-dimensional")
                std = X_train.std(axis=0)
                keep = np.flatnonzero(std > 1e-10)
                if not len(keep):
                    raise ValueError("All design-matrix columns are constant")
                kept = X_train[:, keep]
                mean = np.zeros(len(keep), dtype=float)
                scale = np.ones(len(keep), dtype=float)
                for j in range(len(keep)):
                    unique = np.unique(kept[:, j])
                    binary = len(unique) <= 2 and np.all(np.isin(unique, [0.0, 1.0]))
                    if not binary:
                        mean[j] = kept[:, j].mean()
                        scale[j] = kept[:, j].std()
                        if scale[j] <= 1e-10:
                            scale[j] = 1.0

                transformed_blocks = {}
                source_positions = {}
                original_to_transformed = {int(original): j for j, original in enumerate(keep)}
                for block, original_indices in blocks.items():
                    original_indices = np.asarray(original_indices, dtype=int)
                    kept_original = [idx for idx in original_indices if int(idx) in original_to_transformed]
                    transformed_blocks[block] = np.asarray(
                        [original_to_transformed[int(idx)] for idx in kept_original], dtype=int
                    )
                    source_positions[block] = np.asarray(
                        [int(np.flatnonzero(original_indices == idx)[0]) for idx in kept_original], dtype=int
                    )
                reward_indices = transformed_blocks.get("reward", np.array([], dtype=int))
                if not len(reward_indices):
                    raise ValueError("Reward block has no varying training columns")
                reward_absent = (0.0 - mean[reward_indices]) / scale[reward_indices]
                kept_names = [names[i] for i in keep] if names is not None else [f"x{i}" for i in keep]
                return Transformer(
                    keep_indices=keep,
                    mean=mean,
                    scale=scale,
                    blocks=transformed_blocks,
                    block_source_positions=source_positions,
                    reward_indices=reward_indices,
                    reward_absent=reward_absent,
                    names=kept_names,
                )


            def apply_transformer(X, transformer):
                X = np.asarray(X, dtype=float)
                if X.ndim != 2 or X.shape[1] <= transformer.keep_indices.max():
                    raise ValueError("Design matrix is incompatible with transformer")
                kept = X[:, transformer.keep_indices]
                if not np.isfinite(kept).all():
                    raise ValueError("Design matrix contains non-finite values")
                return ((kept - transformer.mean) / transformer.scale).astype(np.float32)


            def transform_replacement_block(raw_block, transformer, block_name):
                raw_block = np.asarray(raw_block, dtype=float)
                transformed_indices = transformer.blocks[block_name]
                source_positions = transformer.block_source_positions[block_name]
                values = raw_block[:, source_positions]
                return ((values - transformer.mean[transformed_indices]) /
                        transformer.scale[transformed_indices]).astype(np.float32)


            def zero_reward_block(X, transformer):
                zeroed = np.array(X, copy=True)
                zeroed[:, transformer.reward_indices] = transformer.reward_absent
                return zeroed


            def regression_metrics(y_true, y_pred):
                y_true = np.asarray(y_true, dtype=float)
                y_pred = np.asarray(y_pred, dtype=float)
                if y_true.shape != y_pred.shape or y_true.ndim != 2:
                    raise ValueError("Targets and predictions must have the same 2D shape")
                squared = (y_true - y_pred) ** 2
                mse = squared.mean(axis=0)
                numerator = squared.sum(axis=0)
                denominator = ((y_true - y_true.mean(axis=0)) ** 2).sum(axis=0)
                r2 = np.full(y_true.shape[1], np.nan, dtype=float)
                valid = denominator > 0
                r2[valid] = 1.0 - numerator[valid] / denominator[valid]
                return mse, r2


            def fit_ridge_closed_form(X, Y, alpha):
                X = np.asarray(X, dtype=np.float64)
                Y = np.asarray(Y, dtype=np.float64)
                if X.ndim != 2 or Y.ndim != 2 or len(X) != len(Y):
                    raise ValueError("X and Y must be aligned two-dimensional arrays")
                x_mean, y_mean = X.mean(axis=0), Y.mean(axis=0)
                Xc, Yc = X - x_mean, Y - y_mean
                gram = Xc.T @ Xc
                gram.flat[:: gram.shape[0] + 1] += float(alpha)
                coef = linalg.solve(gram, Xc.T @ Yc, assume_a="pos", check_finite=False)
                intercept = y_mean - x_mean @ coef
                return RidgeFit(coef=coef, intercept=intercept, alpha=float(alpha))


            def select_alpha(X, Y, groups, alphas=ALPHAS, n_splits=3):
                X, Y, groups = np.asarray(X), np.asarray(Y), np.asarray(groups)
                unique_groups = np.unique(groups)
                splits = min(int(n_splits), len(unique_groups))
                if splits < 2:
                    raise ValueError("At least two training trials are needed for alpha selection")
                splitter = GroupKFold(n_splits=splits)
                fold_scores = np.empty((len(alphas), splits), dtype=float)
                for fold, (fit_idx, val_idx) in enumerate(splitter.split(X, groups=groups)):
                    for a, alpha in enumerate(alphas):
                        model = fit_ridge_closed_form(X[fit_idx], Y[fit_idx], alpha)
                        mse, _ = regression_metrics(Y[val_idx], model.predict(X[val_idx]))
                        fold_scores[a, fold] = np.nanmean(mse)
                mean_scores = fold_scores.mean(axis=1)
                best = int(np.argmin(mean_scores))
                return float(alphas[best]), fold_scores


            def fit_reward_models(X, Y, train_mask, test_mask, transformer, alpha):
                X, Y = np.asarray(X), np.asarray(Y)
                reward_idx = transformer.reward_indices
                reduced_idx = np.setdiff1d(np.arange(X.shape[1]), reward_idx)
                full_fit = fit_ridge_closed_form(X[train_mask], Y[train_mask], alpha)
                full_pred = full_fit.predict(X[test_mask])
                mse_full, r2_full = regression_metrics(Y[test_mask], full_pred)

                zero_pred = full_fit.predict(zero_reward_block(X[test_mask], transformer))
                mse_zero, r2_zero = regression_metrics(Y[test_mask], zero_pred)

                reduced_fit = fit_ridge_closed_form(
                    X[train_mask][:, reduced_idx], Y[train_mask], alpha
                )
                reduced_pred = reduced_fit.predict(X[test_mask][:, reduced_idx])
                mse_reduced, r2_reduced = regression_metrics(Y[test_mask], reduced_pred)
                return ModelResults(
                    full_fit=full_fit,
                    reduced_fit=reduced_fit,
                    reduced_indices=reduced_idx,
                    mse_full=mse_full,
                    r2_full=r2_full,
                    mse_zero=mse_zero,
                    r2_zero=r2_zero,
                    mse_reduced=mse_reduced,
                    r2_reduced=r2_reduced,
                    delta_mse_zero=mse_zero - mse_full,
                    delta_mse_refit=mse_reduced - mse_full,
                    delta_r2_refit=r2_full - r2_reduced,
                )


            def permutation_pvalues(observed, null):
                observed = np.asarray(observed, dtype=float)[None, :]
                null = np.asarray(null, dtype=float)
                if null.ndim != 2 or null.shape[1] != observed.shape[1]:
                    raise ValueError("Permutation null must be permutations × neurons")
                return (1 + np.sum(null >= observed, axis=0)) / (null.shape[0] + 1)
            """,
            tags=("unit-testable",),
        ),
        md(
            """
            ## 5. Ridge encoding model

            The first, third, fifth, … observed trials train the model; the alternating trials are
            held out. This matches Zhong's supplied `ft_trInd_odd`/`ft_trInd_even` convention even
            though trial IDs are zero-based. Three grouped folds inside the training trials choose
            one shared ridge alpha. The final even-trial set is never used for tuning.
            """
        ),
        code(
            r"""
            def permute_reward_events(reward_events, trial_starts, trial_ends, rng):
                reward_events = np.asarray(reward_events, dtype=float)
                starts = np.asarray(trial_starts, dtype=float)
                ends = np.asarray(trial_ends, dtype=float)
                if not (len(reward_events) == len(starts) == len(ends)):
                    raise ValueError("RewardFr, StartFr, and EndFr must align by trial")
                valid = np.isfinite(reward_events) & np.isfinite(starts) & np.isfinite(ends)
                if valid.sum() < 2:
                    raise ValueError("At least two rewarded trials are required for permutation")
                offsets = reward_events[valid] - starts[valid]
                permuted = rng.permutation(offsets)
                new_events = starts[valid] + permuted
                new_events = np.clip(new_events, starts[valid], ends[valid])
                return new_events


            def _block_ridge_prediction(X0_train, R_train, Y_train, X0_test, R_test, alpha):
                '''Exact ridge prediction using a nuisance/reward block Schur complement.'''
                X0_train = np.asarray(X0_train, dtype=np.float64)
                R_train = np.asarray(R_train, dtype=np.float64)
                Y_train = np.asarray(Y_train, dtype=np.float64)
                X0_test = np.asarray(X0_test, dtype=np.float64)
                R_test = np.asarray(R_test, dtype=np.float64)
                x0_mean, r_mean, y_mean = (
                    X0_train.mean(axis=0), R_train.mean(axis=0), Y_train.mean(axis=0)
                )
                X0c, Rc, Yc = X0_train - x0_mean, R_train - r_mean, Y_train - y_mean
                A = X0c.T @ X0c
                A.flat[:: A.shape[0] + 1] += float(alpha)
                C = X0c.T @ Rc
                E = X0c.T @ Yc
                AinvC = linalg.solve(A, C, assume_a="pos", check_finite=False)
                AinvE = linalg.solve(A, E, assume_a="pos", check_finite=False)
                S = Rc.T @ Rc
                S.flat[:: S.shape[0] + 1] += float(alpha)
                S -= C.T @ AinvC
                rhs = Rc.T @ Yc - C.T @ AinvE
                beta_r = linalg.solve(S, rhs, assume_a="pos", check_finite=False)
                beta_0 = AinvE - AinvC @ beta_r
                intercept = y_mean - x0_mean @ beta_0 - r_mean @ beta_r
                return X0_test @ beta_0 + R_test @ beta_r + intercept


            def reward_permutation_null(
                X, Y, train_mask, test_mask, transformer, design, beh,
                alpha, mse_reduced, n_permutations=199, seed=42, progress=True,
            ):
                reward_idx = transformer.reward_indices
                nuisance_idx = np.setdiff1d(np.arange(X.shape[1]), reward_idx)
                X0_train, X0_test = X[train_mask][:, nuisance_idx], X[test_mask][:, nuisance_idx]
                Y_train, Y_test = Y[train_mask], Y[test_mask]
                rng = np.random.default_rng(seed)
                null = np.empty((n_permutations, Y.shape[1]), dtype=np.float32)
                started = time.perf_counter()
                for permutation in range(n_permutations):
                    events = permute_reward_events(
                        beh["RewardFr"], beh["StartFr"], beh["EndFr"], rng
                    )
                    raw_reward = event_basis(
                        len(X), events, design.frame_rate, -3.0, 3.0, 8
                    )
                    R = transform_replacement_block(raw_reward, transformer, "reward")
                    pred = _block_ridge_prediction(
                        X0_train, R[train_mask], Y_train,
                        X0_test, R[test_mask], alpha,
                    )
                    mse_permuted, _ = regression_metrics(Y_test, pred)
                    null[permutation] = (mse_reduced - mse_permuted).astype(np.float32)
                    if progress and ((permutation + 1) % 20 == 0 or permutation == 0):
                        elapsed = time.perf_counter() - started
                        print(f"Permutation {permutation + 1}/{n_permutations} | {elapsed:.1f} s")
                return null


            def wilson_interval(successes, total, z=1.96):
                if total <= 0:
                    return np.nan, np.nan
                p = successes / total
                denom = 1 + z * z / total
                center = (p + z * z / (2 * total)) / denom
                half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
                return center - half, center + half


            def run_synthetic_recovery_test():
                rng = np.random.default_rng(7)
                n_trials, frames_per_trial = 40, 15
                n_frames = n_trials * frames_per_trial
                trials = np.repeat(np.arange(n_trials), frames_per_trial)
                train, test = odd_even_masks(trials.astype(float))
                starts = np.arange(n_trials) * frames_per_trial
                ends = starts + frames_per_trial - 1
                events = starts + np.where(np.arange(n_trials) % 3 == 0, 4, 10)
                reward = event_basis(n_frames, events, 5.0, -1.0, 1.0, 4)
                nuisance = rng.normal(size=(n_frames, 3))
                raw = np.column_stack([nuisance, reward])
                blocks = {"nuisance": np.arange(3), "reward": np.arange(3, 7)}
                transformer = fit_transformer(raw[train], blocks)
                X = apply_transformer(raw, transformer)
                y_injected = 4.0 * reward[:, 2] + 0.4 * nuisance[:, 0] + rng.normal(0, 0.15, n_frames)
                null_targets = nuisance @ rng.normal(size=(3, 8)) + rng.normal(0, 0.8, (n_frames, 8))
                Y = np.column_stack([y_injected, null_targets]).astype(np.float32)
                results = fit_reward_models(X, Y, train, test, transformer, alpha=0.1)
                design = DesignMatrix(raw=raw, names=[f"x{i}" for i in range(7)],
                                      blocks=blocks, frame_rate=5.0)
                synthetic_beh = {"RewardFr": events, "StartFr": starts, "EndFr": ends}
                null = reward_permutation_null(
                    X, Y, train, test, transformer, design, synthetic_beh, 0.1,
                    results.mse_reduced, n_permutations=39, seed=9, progress=False,
                )
                p = permutation_pvalues(results.delta_mse_refit, null)
                output = {
                    "injected_delta_mse": float(results.delta_mse_refit[0]),
                    "injected_p": float(p[0]),
                    "median_null_p": float(np.median(p[1:])),
                }
                if not (output["injected_delta_mse"] > 0 and
                        output["injected_p"] < output["median_null_p"]):
                    raise AssertionError(f"Synthetic recovery failed: {output}")
                return output
            """,
            tags=("unit-testable",),
        ),
        md(
            """
            ## 6. Reward ablation and permutation test

            Two ablations answer different questions:

            - **Zero-out screen:** keep fitted weights fixed and replace reward input with its
              transformed reward-absent value. This is fast but can over-credit reward.
            - **Reduced-model refit (primary):** drop the entire reward block and refit nuisance
              weights. `ΔMSE = MSE_reduced − MSE_full` estimates reward's unique held-out value.

            For inference, reward timing offsets are shuffled among rewarded trials. This keeps
            reward on the rewarded stimulus while breaking exact timing. All 1,000 neurons receive
            all permutations; the zero-out result never selects which neurons are tested.
            """
        ),
        code(
            r"""
            synthetic_check = run_synthetic_recovery_test()
            print("Synthetic recovery passed:", synthetic_check)
            """
        ),
        code(
            r"""
            run_started = time.perf_counter()
            paths = {
                key: download_figshare_file(file_id, filename, size)
                for key, (file_id, filename, size) in FILES.items()
            }

            behavior_sessions = np.load(paths["behavior"], allow_pickle=True).item()
            if SESSION not in behavior_sessions:
                raise KeyError(f"Session {SESSION!r} not found; available: {list(behavior_sessions)}")
            beh_original = behavior_sessions[SESSION]

            # The official file includes an unused sklearn model; U and V are plain arrays.
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="Trying to unpickle estimator TruncatedSVD")
                svd_file = np.load(paths["svd"], allow_pickle=True).item()
            svd = {"U": np.asarray(svd_file["U"]), "V": np.asarray(svd_file["V"])}
            retin = np.load(paths["retinotopy"], allow_pickle=False)

            n_frames = svd["V"].shape[1]
            beh = align_behavior_frames(beh_original, n_frames)
            frame_rate = infer_frame_rate(beh["ft"])
            regions_all = map_regions(retin["iarea"])

            qc = pd.DataFrame({
                "item": ["neural frames", "behavior trials", "reward events", "lick events",
                         "cue events", "frame rate (Hz)", "SVD neurons"],
                "value": [n_frames, int(beh["ntrials"]), int(np.isfinite(beh["RewardFr"]).sum()),
                          len(beh["LickFr"]), int(np.isfinite(beh["SoundFr"]).sum()),
                          round(frame_rate, 3), svd["U"].shape[1]],
            })
            display(qc)
            """
        ),
        code(
            r"""
            selected_indices, selected_regions = balanced_sample(
                regions_all, N_PER_REGION, seed=SEED
            )
            Y = reconstruct_selected(svd, selected_indices)
            if Y.shape != (n_frames, 4 * N_PER_REGION):
                raise ValueError(f"Unexpected reconstructed target shape: {Y.shape}")
            if not np.isfinite(Y).all():
                raise ValueError("Reconstructed neural targets contain non-finite values")

            region_counts = pd.Series(selected_regions).value_counts().reindex(AREA_CODES)
            display(region_counts.rename("selected neurons").to_frame())
            print(f"Target Y shape: {Y.shape} (frames × neurons), dtype={Y.dtype}")
            """
        ),
        code(
            r"""
            train_mask, test_mask = odd_even_masks(beh["ft_trInd"])
            supplied_train = np.asarray(beh["ft_trInd_odd"], dtype=bool)
            supplied_test = np.asarray(beh["ft_trInd_even"], dtype=bool)
            if not (np.array_equal(train_mask, supplied_train) and
                    np.array_equal(test_mask, supplied_test)):
                raise ValueError("Derived alternating-trial masks do not match Zhong's supplied masks")

            design = build_design_matrix(beh, train_mask)
            transformer = fit_transformer(
                design.raw[train_mask], design.blocks, design.names
            )
            X = apply_transformer(design.raw, transformer)
            if not np.isfinite(X).all():
                raise ValueError("Transformed design matrix contains non-finite values")

            frame_trials = np.asarray(beh["ft_trInd"], dtype=float)
            trial_ids = np.zeros(len(frame_trials), dtype=np.int64)
            finite_trials = np.isfinite(frame_trials)
            trial_ids[finite_trials] = np.rint(frame_trials[finite_trials]).astype(np.int64)
            train_groups = trial_ids[train_mask]
            manifest = pd.DataFrame([
                {
                    "block": block,
                    "raw columns": len(indices),
                    "retained columns": len(transformer.blocks.get(block, [])),
                }
                for block, indices in design.blocks.items()
            ])
            display(manifest)
            print(f"Raw design: {design.raw.shape}; transformed design: {X.shape}")
            print(f"Train frames: {train_mask.sum():,}; held-out frames: {test_mask.sum():,}")

            # Compact diagnostic: representative columns only, so labels remain readable.
            diagnostic_idx = np.unique(np.linspace(0, X.shape[1] - 1, min(30, X.shape[1])).astype(int))
            corr = np.corrcoef(X[train_mask][:, diagnostic_idx], rowvar=False)
            fig, ax = plt.subplots(figsize=(9, 7))
            sns.heatmap(corr, vmin=-1, vmax=1, cmap="vlag", center=0, ax=ax,
                        xticklabels=[transformer.names[i] for i in diagnostic_idx],
                        yticklabels=[transformer.names[i] for i in diagnostic_idx])
            ax.set_title("Representative training-feature correlations")
            plt.tight_layout()
            plt.show()
            """
        ),
        code(
            r"""
            print("Selecting ridge alpha using grouped folds inside training trials …")
            alpha_started = time.perf_counter()
            best_alpha, fold_scores = select_alpha(
                X[train_mask], Y[train_mask], train_groups, ALPHAS, n_splits=3
            )
            alpha_seconds = time.perf_counter() - alpha_started
            score_mean = fold_scores.mean(axis=1)
            print(f"Selected alpha={best_alpha:g} in {alpha_seconds:.1f} s")

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.semilogx(ALPHAS, score_mean, marker="o")
            ax.axvline(best_alpha, color="tab:red", linestyle="--", label=f"selected {best_alpha:g}")
            ax.set(xlabel="ridge alpha", ylabel="mean validation MSE", title="Training-only alpha selection")
            ax.legend()
            plt.show()

            model_results = fit_reward_models(
                X, Y, train_mask, test_mask, transformer, best_alpha
            )
            print(f"Median held-out MSE: {np.median(model_results.mse_full):.4g}")
            print(f"Median held-out R²: {np.nanmedian(model_results.r2_full):.4g}")
            """
        ),
        code(
            r"""
            print(f"Running {N_PERMUTATIONS} trial-wise reward-timing permutations …")
            permutation_started = time.perf_counter()
            null_delta_mse = reward_permutation_null(
                X, Y, train_mask, test_mask, transformer, design, beh,
                best_alpha, model_results.mse_reduced,
                n_permutations=N_PERMUTATIONS, seed=SEED, progress=True,
            )
            permutation_seconds = time.perf_counter() - permutation_started
            permutation_p = permutation_pvalues(
                model_results.delta_mse_refit, null_delta_mse
            )
            reward_candidate = (
                (model_results.delta_mse_refit > 0) & (permutation_p < 0.05)
            )
            print(f"Permutations completed in {permutation_seconds:.1f} s")
            print(f"Raw p<0.05 candidates: {reward_candidate.sum()} / {len(reward_candidate)}")
            """
        ),
        md(
            """
            ## 7. Results and export

            We inspect prediction quality, compare the quick zero-out effect with the refit effect,
            view example null distributions and reward coefficients, and summarize raw candidate
            percentages by region. The exported table preserves every neuron-level metric.
            """
        ),
        code(
            r"""
            fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
            axes[0].hist(model_results.mse_full, bins=40, color="0.25")
            axes[0].set(xlabel="held-out MSE", ylabel="neurons", title="Full-model error")
            finite_r2 = model_results.r2_full[np.isfinite(model_results.r2_full)]
            axes[1].hist(finite_r2, bins=40, color="tab:blue")
            axes[1].set(xlabel="held-out R²", ylabel="neurons", title="Full-model R²")
            for region in AREA_CODES:
                mask = selected_regions == region
                axes[2].scatter(
                    model_results.delta_mse_zero[mask],
                    model_results.delta_mse_refit[mask],
                    s=15, alpha=0.55, label=region,
                )
            axes[2].axhline(0, color="0.5", linewidth=1)
            axes[2].axvline(0, color="0.5", linewidth=1)
            axes[2].set(xlabel="ΔMSE zero-out", ylabel="ΔMSE refit",
                        title="Reward ablation effects")
            axes[2].legend()
            plt.tight_layout()
            plt.show()
            """
        ),
        code(
            r"""
            reward_coef = model_results.full_fit.coef[transformer.reward_indices].T
            rank = np.argsort(model_results.delta_mse_refit)[::-1]
            examples = rank[: min(4, len(rank))]
            fig, axes = plt.subplots(2, len(examples), figsize=(4 * len(examples), 7))
            axes = np.atleast_2d(axes)
            lag_centers = np.linspace(-3, 3, reward_coef.shape[1])
            for column, neuron in enumerate(examples):
                axes[0, column].hist(null_delta_mse[:, neuron], bins=25, color="0.75")
                axes[0, column].axvline(model_results.delta_mse_refit[neuron], color="tab:red")
                axes[0, column].set_title(
                    f"{selected_regions[neuron]} | p={permutation_p[neuron]:.3f}"
                )
                axes[0, column].set_xlabel("permuted / observed ΔMSE")
                axes[1, column].plot(lag_centers, reward_coef[neuron], marker="o")
                axes[1, column].axhline(0, color="0.5", linewidth=1)
                axes[1, column].set(xlabel="reward lag basis center (s)",
                                    ylabel="ridge coefficient")
            plt.tight_layout()
            plt.show()
            """
        ),
        code(
            r"""
            summary_rows = []
            for region in AREA_CODES:
                mask = selected_regions == region
                successes, total = int(reward_candidate[mask].sum()), int(mask.sum())
                low, high = wilson_interval(successes, total)
                summary_rows.append({
                    "region": region,
                    "candidates": successes,
                    "neurons": total,
                    "percent": 100 * successes / total,
                    "ci_low_percent": 100 * low,
                    "ci_high_percent": 100 * high,
                })
            region_summary = pd.DataFrame(summary_rows)
            display(region_summary)

            fig, ax = plt.subplots(figsize=(7, 4.5))
            centers = region_summary["percent"].to_numpy()
            errors = np.vstack([
                centers - region_summary["ci_low_percent"].to_numpy(),
                region_summary["ci_high_percent"].to_numpy() - centers,
            ])
            ax.bar(region_summary["region"], centers, color=["#4C78A8", "#72B7B2", "#F2CF5B", "#E45756"])
            ax.errorbar(np.arange(len(centers)), centers, yerr=errors, fmt="none", color="black", capsize=4)
            ax.set(ylabel="raw p<0.05 candidates (%)",
                   title="Descriptive reward-encoding candidates by region")
            plt.show()
            print("WARNING: raw neuron-level p-values are uncorrected; this is one mouse/session.")
            """
        ),
        code(
            r"""
            results_df = pd.DataFrame({
                "neuron_index": selected_indices,
                "region": selected_regions,
                "mse_full": model_results.mse_full,
                "r2_full": model_results.r2_full,
                "mse_reduced": model_results.mse_reduced,
                "r2_reduced": model_results.r2_reduced,
                "delta_mse_zero": model_results.delta_mse_zero,
                "delta_mse_refit": model_results.delta_mse_refit,
                "delta_r2_refit": model_results.delta_r2_refit,
                "permutation_p": permutation_p,
                "reward_encoding_candidate": reward_candidate,
            })
            for basis_index in range(reward_coef.shape[1]):
                results_df[f"reward_coef_{basis_index}"] = reward_coef[:, basis_index]
            if not set(RESULT_COLUMNS).issubset(results_df.columns):
                raise AssertionError("Result table is missing required columns")

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            csv_path = OUTPUT_DIR / "reward_encoding_pilot_results.csv"
            json_path = OUTPUT_DIR / "reward_encoding_pilot_run_manifest.json"
            results_df.to_csv(csv_path, index=False)
            run_seconds = time.perf_counter() - run_started
            manifest_out = {
                "session": SESSION,
                "seed": SEED,
                "n_per_region": N_PER_REGION,
                "n_neurons": int(len(selected_indices)),
                "n_permutations": N_PERMUTATIONS,
                "ridge_alpha": best_alpha,
                "train_frames": int(train_mask.sum()),
                "test_frames": int(test_mask.sum()),
                "frame_rate_hz": design.frame_rate,
                "raw_design_columns": int(design.raw.shape[1]),
                "retained_design_columns": int(X.shape[1]),
                "candidate_count": int(reward_candidate.sum()),
                "elapsed_seconds": run_seconds,
                "figshare_files": {
                    key: {"file_id": value[0], "filename": value[1], "bytes": value[2]}
                    for key, value in FILES.items()
                },
                "versions": {
                    "python": platform.python_version(),
                    "numpy": np.__version__,
                    "pandas": pd.__version__,
                    "scikit_learn": sklearn.__version__,
                },
            }
            json_path.write_text(json.dumps(manifest_out, indent=2) + "\n")

            # Read exports back immediately: writing without a parse check is not verification.
            checked_csv = pd.read_csv(csv_path)
            checked_json = json.loads(json_path.read_text())
            if len(checked_csv) != 4 * N_PER_REGION or checked_json["session"] != SESSION:
                raise AssertionError("Export validation failed")

            print(f"Saved {csv_path} ({len(checked_csv)} rows)")
            print(f"Saved {json_path}")
            print(f"Total elapsed time: {run_seconds / 60:.1f} minutes")

            try:
                from google.colab import files as colab_files
            except ImportError:
                colab_files = None
            if colab_files is not None:
                print("Starting browser downloads for the CSV and run manifest …")
                colab_files.download(str(csv_path))
                colab_files.download(str(json_path))
            """
        ),
        md(
            """
            ## Interpretation checklist

            - Positive refit ΔMSE means the full reward block improved held-out prediction beyond
              the other regressors; negative values are allowed and should not be forced to zero.
            - The zero-out effect is a screen, not the classification statistic.
            - A raw permutation `p < 0.05` candidate is exploratory. With 1,000 tests, about 50
              chance positives are possible under a complete null.
            - This pilot cannot test change across days, supervised-versus-unsupervised cohorts,
              or mouse-level regional enrichment. Those require the planned multi-session study.
            - SVD-reconstructed deconvolved activity is the target; it is not raw ΔF/F.
            """
        ),
    ]
    # Stable cell ids make regeneration byte-for-byte deterministic.
    for index, cell in enumerate(nb.cells):
        cell["id"] = f"reward-pilot-{index:03d}"
    return nb


if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(build_notebook(), OUTPUT)
    print(OUTPUT)
