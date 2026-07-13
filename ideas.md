# Project Ideas — Task vs. Unsupervised Plasticity (Zhong et al. 2025)

Interest: the **difference in plasticity between task mice and unsupervised mice**.

> **Two different experiments / datasets — don't conflate them:**
> - **Directions A & B = imaging arm** (Figs 1-4): 19 GCaMP6s mice with cranial windows,
>   neural data. Groups: **Task, Unsupervised, Grating, Naive**.
> - **Direction C = behavior-only arm** (Fig 5): 23 headbar-only mice, NO imaging, licking
>   data only. Groups: **VRn** (naturalistic pretraining), **VRg** (grating pretraining),
>   **No pretraining**. VRn/VRg/none were never recorded — behavior only.
>
> A/B are neural analyses; C is a behavioral (curve-fitting) analysis. Different animals.

Starting point: Fig. 1i — 2D density maps of stimulus-selective neurons (|d'| >= 0.3)
before vs. after learning. The medial-area growth looks nearly identical in task and
unsupervised mice; the grating control does not reproduce it. So the paper's answer to
"what's the difference?" is: little difference in the *representational* plasticity — the
one clean task-only difference is a reward-prediction ramp in anterior HVAs (Fig. 4).

---

## Direction A — Quantify how much plasticity is reward-independent (shared), by region

**Phenomenon:** after learning, stimulus selectivity in medial HVAs rises similarly in task
and unsupervised mice (Fig. 1i,j); grating controls don't reproduce it.

- **Precise aspect:** how much of the task-cohort plasticity is reproduced in the
  unsupervised cohort, resolved region by region — the *amount* AND *shape* of the overlap.
- **Analyses:**
  - Per-region fraction of selective neurons (|d'| >= 0.3), before vs after, task vs
    unsupervised. Quantify overlap as a ratio of effect sizes (unsupervised / task) per region.
  - Coding-direction / similarity-index: does the learned category axis generalize equally
    in both cohorts?
  - Shape check: correlate the *per-region plasticity vector* across cohorts — do the same
    regions/neuron-types change, not just the same total amount?
- **Fresh angles (to avoid just re-running the paper):** does the overlap decay across
  learning stages (Train1 -> Train2)? is it uniform across medial sub-areas (PM / AM / MMA)?
- **Data:** PCA-compressed responses + corridor labels + cohort labels + before/after. No
  reward-timing needed — the friendlier data requirement.
- **Rigor:** train/test split for every d'; shuffle/label-swap control; watch multiple
  comparisons across regions.
- **One-sentence goal:** Quantify, region by region, what fraction of the learning-related
  selectivity change seen in task mice is reproduced in unsupervised mice, and whether the
  overlap is uniform across medial sub-areas and stable across learning stages.

## Direction B — Isolate the reward-dependent (supervised) plasticity and localize it

**Phenomenon:** a reward-prediction signal appears in anterior HVAs only in task mice, ramps
before reward and is suppressed by it (Fig. 4).

- **Precise aspect:** what plasticity exists ONLY in the rewarded cohort, and where it sits.
- **Analyses:**
  - d'(late vs early) reward-prediction index: compare leaf1 trials with cue/reward late vs
    early to isolate *anticipatory* activity; select neurons at >= 0.3.
  - Enrichment of these neurons by region, task vs unsupervised (paper: anterior p=0.0069 vs
    0.708). Reproduce and probe finer anatomy.
  - Dissociate from licking: is the signal choice-predictive on unrewarded trials, and does
    it ramp *before* the first lick?
- **Data:** needs reward/cue timing per trial AND lick data, not just corridor identity —
  heavier requirement. Confirm it's in the release before committing.
- **Rigor:** train/test neuron selection; shuffle control; separate anticipatory from motor
  (running/lick) confounds.
- **One-sentence goal:** Identify neurons whose plasticity is present only with reward
  (a reward-anticipation signal), quantify their enrichment across visual areas in task vs
  unsupervised mice, and confirm the signal reflects expectation rather than licking.

**A vs B in one line:** A = measure how much of the change is reward-free (shared), by region.
B = find and localize the change that only reward produces.

---

## Rigor reminders (both directions)

- **Train/test split, reflexively.** Select neurons on one half, read out on held-out
  trials — even for a simple selectivity fraction.
- **Circularity trap.** Don't select neurons in one cohort then "discover" they differ;
  build a shuffle / label-swap control in from the start.

## Week-1 next steps (we're just exploring)

1. Run the loading notebook; get responses to load and plot *something*.
2. Check what's in the data: can we tell task vs. unsupervised mice? Can we see *when* the
   reward/cue happens per trial? -> if yes, Direction B is on the table; if that timing is a
   pain to get, Direction A is the friendlier start.
3. Make one plot we understand: a few neurons, response in leaf corridor vs. circle corridor.

**Ask the Project TA early:** "How do I get the reward/cue timing per trial?" — the answer
basically decides A vs. B.

---

## Direction C — "How fast do they learn, and what does pretraining change?"

Based on Fig. 5 (behavior-only arm): 23 mice, 3 cohorts —
**VRn** (naturalistic pretraining, n=11), **VRg** (grating pretraining, n=7),
**No pretraining** (n=5); 10 days pretraining then 5 days rewarded task.

### Panel f — the learning curve (this is the core panel)

- **Y-axis: Delta Lick = (% reward trials with a lick) - (% non-reward trials with a lick).**
  A discrimination score: 0 = licks equally in both corridors (learned nothing);
  ~100 = perfect (licks every reward trial, never in non-reward). Collapses panel e's
  two lines (blue reward, red non-reward) into one number per mouse per day.
- **X-axis:** passive reward (baseline), then active-reward days 1-4.
- Each dot = one mouse. dark grey = no pretraining, light grey = VRg, pink = VRn.
  Lines = cohort mean +/- s.e.m.
- **Stars:** ** at passive reward and **/* at day 1 = VRn significantly ahead early.
  Days 2-4 no stars — all cohorts converge to ~75-80%.
- **Story:** pink (naturalistic-pretrained) mice discriminate better before real training
  even starts and on day 1; advantage fades by day 3-4.
- **The open gap:** is pink faster because it STARTS higher (head start) or CLIMBS steeper
  (faster rate)? Panel f can't separate them — that's the opening.

Related panels: **e** = raw blue/red components f is built from; **g** = first-lick position
sliding into the reward zone over days (a spatial-timing learning curve); **h** = trial
counts equal across cohorts (rules out "learned faster by doing more trials").

### Goal (Step-1 / W2D1 Tutorial-1 framing)

- **Phenomenon:** naturalistic-pretrained mice learn the discrimination faster (Fig. 5f).
- **Precise aspect:** the shape + parameters of the Delta-lick learning curve — specifically
  WHICH parameter pretraining changes: starting point vs rate.
- **Not addressing yet:** the neural/synaptic mechanism; behavior only.
- **Evaluation:** fit competing curve models (linear vs exponential vs power) per mouse,
  compare with AIC; fitted curve must predict held-out days/trials; then test whether the
  starting-point vs rate parameter differs across cohorts.
- **Data:** Fig. 5 behavioral licking across the 3 cohorts (VERIFY it's in the release).

**One-sentence goal:** Characterize the behavioral learning curve (reward-vs-non-reward lick
discrimination over time) in pretrained vs non-pretrained mice, and determine whether
unsupervised pretraining accelerates learning by raising the starting point or by increasing
the learning rate.

### Candidate hypotheses (for Step 4 later)

- **H1 (head start):** pretraining shifts the intercept P0, not the rate — representation
  already there.
- **H2 (faster dynamics):** pretraining shrinks the time-constant tau, same start — learning
  itself is faster.
- **H3 (curve shape):** individual learning curves fit exponential better than linear/power
  (Heathcote et al. 2000 — power-law group curves are an averaging artifact; fit per-mouse).

### Candidate curve models

- Linear: `P(t) = a + b*t` (null to beat).
- Exponential to asymptote: `P(t) = Pinf - (Pinf - P0)*exp(-t/tau)` — gives all three knobs
  (P0 start, tau rate, Pinf asymptote) as parameters. Workhorse; = error-correction learning.
- Power law: `P(t) = a*t^b` — the "power law of practice"; watch the averaging artifact.

### Rigor

- **Fit per-animal, then compare parameters** across cohorts (never fit pooled data).
- **Model comparison with AIC/BIC** (same method as the Laquitaine behavior template).
- **Train/test:** fit early trials/days, predict held-out.
- **Small n (5-11):** any parameter difference needs a caveat + bootstrap.
- **Panel f has only 5 time-points** — enough for "starts higher vs converges later", too thin
  to fit a curve SHAPE. Curve-shape (linear vs nonlinear) needs the WITHIN-SESSION
  trial-by-trial data (Ext. Fig. 9).

### Big-idea hook

**Transfer learning** (NMA big idea #7): "pretrain on unlabeled data -> learn the real task
faster" is the GPT/BERT trick. You'd be measuring HOW the transfer shows up in the curve.
