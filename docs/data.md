# The `beh` behavioral dataframe — plain-language guide

`beh` is a Python dict loaded per session, e.g.:

```python
beh = np.load('Beh_sup_train1_before_learning.npy', allow_pickle=1).item()[sup_bef]
```

**The task:** a mouse runs down a virtual-reality corridor. The corridor walls
show a texture (a **stimulus**). One stimulus (leaf1 in the supervised task) is
the **rewarded** one — if the mouse licks in that corridor it gets water. A
**sound cue** plays partway down. After ~40 units of corridor the mouse enters a
blank **gray space**, then the next trial's corridor begins.

Two time bases run through the data, and it matters which one a variable uses:

- **Behavioral time** — the raw movement/lick log (fine-grained).
- **Neural frames** — one sample per two-photon imaging frame. **Anything named
  `ft_...` or `...Fr` is already aligned to neural frames**, so it lines up
  row-for-row with the neural activity. These are the ones you build the model on.

---

## 1. Trial structure

| Variable | Meaning |
|----------|---------|
| `ntrials` | Number of trials (corridors) in the session. |
| `trInd` | Index of each trial. |
| `trInd_odd` / `trInd_even` | Odd / even trial indices — **use these for the train/test split** (splitting by trial, not by frame, avoids leakage). |
| `Trial_start_time` / `Trial_end_time` | When the animal entered / left each corridor (behavioral time). |
| `TrialStim` | Stimulus name of each trial. |
| `StimTrial` | For each stimulus, which trials showed it. |
| `StimFrame` | For each stimulus, which neural frames belong to it. |

## 2. Stimulus / corridor identity

| Variable | Meaning |
|----------|---------|
| `stim_id` | Numeric stimulus code: `0`=circle1, `1`=circle2, `2`=leaf1, `3`=leaf2, `4`=leaf3, `5`=leaf1_swap1, `6`=leaf1_swap2. In the supervised task **leaf1 = rewarded**, circle1 = not rewarded. |
| `WallName` | Name of the stimulus shown in each corridor (per trial). |
| `UniqWalls` | The set of stimulus names used in the whole session. |
| `ft_WallID` | **Stimulus of each neural frame** — the frame-aligned version, this is your stimulus regressor. |
| `WallType` | Stimulus category — **ignore** (doesn't apply here). |
| `WallIsProbe` | Whether it's a catch trial — **ignore**. |

## 3. Position

| Variable | Meaning |
|----------|---------|
| `ft_Pos` | **Position inside the current corridor** for each neural frame. ~0–40 = textured wall, ~40–60 = gray space. Your position regressor. |
| `ft_PosCum` | Cumulative position across the whole session (keeps counting up). |
| `VRpos` / `VRposCum` | Position / cumulative position in VR (behavioral time). |
| `VRposTime` | Timestamps for `VRpos`. |
| `ft_GraySpc` | True when the animal is in the gray space (frame-aligned). |
| `ft_CorrSpc` | True when the animal is in the textured corridor (frame-aligned). |
| `Gray_space_time` | Time the animal entered the gray space. |

## 4. Running / movement

| Variable | Meaning |
|----------|---------|
| `ft_RunSpeed` / `RunFr` | **Running speed per neural frame** (same thing, two names). Your velocity regressor. |
| `ft_isMoving` | True when the animal is moving (`ft_move > 0`), frame-aligned. |
| `ft_move` | Frame-to-frame change in cumulative VR position. |
| `ft_RunCum` | Cumulative running distance per neural frame. |
| `run_pos` | Running speed reshaped into trials × positions. |
| `SubjMove` | Sub-dict of raw movement (behavioral time): `SubjMTime` (timestamps), `SubjMPos` / `SubjMPosCum` (position), `SubjM_pitch` (forward speed), `SubjM_roll` / `SubjM_yaw` (turning speed), `SubjM_pitch_cum` (total forward distance). Usually you'll use the `ft_`/`RunFr` versions instead. |

## 5. Reward  ← the variable of interest

| Variable | Meaning |
|----------|---------|
| `RewardFr` | **Neural frame when reward was delivered**, one value per trial; `NaN` for trials with no reward. This is what you time-lock the reward regressor to. |
| `isRew` | True/False: was this a reward trial? |
| `RewTime` | Reward delivery time (behavioral time; only meaningful in the reward corridor). |
| `RewPos` | Position of reward delivery; `NaN` in non-reward corridors. |

> **Confound to remember:** the rewarded corridor *is* the leaf1 stimulus, so
> reward and stimulus identity overlap. Reward is only separable because it
> happens at one *moment* (`RewardFr`) — model it as a short kernel around that
> frame, with stimulus, position, cue, and lick all in the model too. See
> `Reward_Mode` below.

## 6. Licking

| Variable | Meaning |
|----------|---------|
| `LickFr` | **Neural frame of each lick** — your lick regressor (a motor/behavior control). |
| `LickTime` | Time of each lick (behavioral time). |
| `LickPos` | Position of each lick. |
| `LickTrind` | Which trial each lick belongs to. |
| `Lick_wallName` | Which stimulus the animal was in for each lick. |

## 7. Sound cue

| Variable | Meaning |
|----------|---------|
| `SoundFr` | **Neural frame when the sound cue played** — your cue regressor. |
| `SoundDelayFr` | Cue frame plus a delay setting (equals `SoundFr` if delay = 0). |
| `SoundPos` | Position of the cue. |
| `SoundDelPos` | Position matching `SoundDelayFr`. |
| `SoundTime` / `SoundTimeDelay` | Cue time / delayed cue time (behavioral time). |
| `BefCueFr` / `AftCueFr` | True for frames before / after the cue was delivered. |

## 8. Other neural-frame landmarks

| Variable | Meaning |
|----------|---------|
| `ft` | Timestamp of each neural frame. |
| `ft_trInd` | Which trial each neural frame belongs to (`NaN` = outside recorded behavior). |
| `ft_trInd_odd` / `ft_trInd_even` | Frames belonging to odd / even trials — **frame-aligned train/test masks.** |
| `StartFr` | Frame the animal entered each corridor. |
| `GrayFr` | Frame the animal entered the gray space. |
| `EndFr` | Frame the animal left each corridor. |

## 9. Settings (fixed per session)

| Variable | Meaning |
|----------|---------|
| `Corridor_Length` | Length of the corridor. |
| `Texture_Length` | Length of the textured part. |
| `Gray_Space_length` | Length of the gray space. |
| `Reward_Mode` | **Passive** (water given automatically) or **active** (water triggered by licking). If active, lick and reward are tightly coupled — the lick regressor is essential. |
| `Reward_Delay_ms` | Reward delay setting; the actual delivery time is in `RewTime` / `RewardFr`. |

---

### Quick pick for the encoding model

| Role | Use |
|------|-----|
| Target y | deconvolved spikes (`example_raw_data`), frames × neurons |
| Reward | `RewardFr` |
| Stimulus | `ft_WallID` |
| Position | `ft_Pos` |
| Velocity | `ft_RunSpeed` (+ `ft_isMoving`) |
| Lick (control) | `LickFr` |
| Cue (control) | `SoundFr` / `SoundDelayFr` |
| Train/test split | `ft_trInd_odd` / `ft_trInd_even` |
