# Methodology

The experiments ask whether examples improve predictions on independent queries. Within-task adaptation, pretraining progress, mechanism attribution and real-world transfer are separate questions with separate controls.

## Common numerical-regression protocol

Each task provides ordinary input/outcome pairs. Query labels are withheld from adaptation. Shared weights stay frozen during evaluation; only task-local weights or context change. K curves use nested support prefixes, generally K4/8/16/32/64, disjoint from query rows. D4/8/16/32 is the main synthetic coverage; D6/12/24 is a withheld-dimensional track in later pilots.

Learner-side centering/scaling and imputation use supports only. Numerical scale is generally twice the population standard deviation, with a fallback of one for zero scales. Some synthetic generators center/scale the complete generated function pool as a **generative prior**. That is disclosed separately from learner normalization; these studies do not establish strictly streaming normalization.

The usual NMSE is each function's physical-unit mean query squared error divided by that function's query-target population variance, with a small floor where specified, then averaged under that study's declared family/dimension/support weighting. Reporting query variance never supplies query labels to the learner. Equal family weighting and occurrence weighting can differ across studies; study cards specify which estimate is shown.

Error reduction is `100 × (1 − candidate_error/reference_error)`. Positive favors the named candidate; negative is a regression. This is a percentage of **error**, not accuracy percentage points. The transformation is applied to aggregate errors, not averaged per-function percentage gains. Scientific comparisons never combine errors from different banks.

## Historical 1 November original-lineage plateau repair

Seeds **1811 and 1877** restore original fresh-experience 4K weights and AdamW moments. Twenty separately trained continuations each add 4,000 steps (80,000 continuation optimizer steps in total), batch eight, ordinary normalized scalar query MSE. Original parameters use constant 3e−5 LR; new small Tiny credit/retrieval parameters and matched current readers use a declared 3e−4 group. AdamW uses betas (.9,.999), epsilon 1e−8 and weight decay 1e−4.

Arms share saved function occurrences, batch order, positions, feature tags and D/K schedule. CC distribution interventions alone replace roughly half the nonlinear occurrences with scaffolded laws. They test a **difficulty/composition bundle**, not isolated diversity, frequency or sparsity effects. Clipping-only arms change threshold 1→5.

Fresh development/final banks were generated and hash-locked before candidate training. The generator root is **1000013269457**, with development/final bank roots **1000113269457 / 1000213269457**; the final bank hash is in [provenance](../benchmarks/provenance.json). They contain **604 / 1,176** function/task draws, including real support draws. Familiar synthetic counts are 256 / 512; excluded 64 / 128; structural 32 / 64; unseen-D 96 / 192; controlled 124 / 248; each of four real datasets has eight draws. Original-prior families are affine, tanh-ridge, random neural and Fourier. Most synthetic tasks have 64 queries; some controlled cases have 128. Real counts are in the study card.

The primary endpoint is familiar **all K**. K16/32/64 is secondary. A common candidate could advance only if both seeds met all criteria: at least 5% all-K improvement over both strongest matched control and original 8K with positive intervals; at least 1% 6K→8K progress with positive intervals; excluded/structure/real safeguards and every-K familiar nonregression. **No candidate passed.** The nominal development-selected Tiny_Global and CC_G were reported on the independent final bank without final-driven reselection. No 10K/12K extension or promotion occurred.

## Current 32K→64K continuation

Exactly one 32K broader-prior parent per architecture was selected using a locked synthetic-validation aggregate: TinyMind **seed 1877**, CC **seed 1811**. Confirmation scores and real labels did not select these parents. Both continued from saved weights and AdamW moments to **64,000 cumulative optimizer steps**. The separately validation-selected final checkpoints were Tiny 62K / CC 64K; the current endpoint and TabArena comparisons deliberately report **fixed 64K** for both.

The first 32K steps used physical batch eight (**256,000 presentations**). The next 32K used physical batch 64 without accumulation (**2,048,000 additional presentations**), for **2,304,000 cumulative synthetic task presentations per model**. Dataset fingerprints showed no duplicate generated datasets in the continuation, but this does not prove unique mathematical functions or unique cumulative tasks.

The continuation prior mixed **40% original laws**, **40% preserved broader laws** and **20% expanded robust laws**. Original laws include affine/ridge/neural/Fourier; the preserved group covers composition, piecewise, discontinuous, oscillatory, interacting and causal tasks; expanded laws include sparse additive, pair-product, soft-gated and robust structural-causal tasks with noise/input variations. Training uses D4/8/16/32 and intermediate dimensions; confirmation separates familiar, novel-relationship, excluded-operation, unseen-structure, unseen-dimensional and expanded-robustness tracks. Their generator labels are operational categories, not proof of arbitrary new-concept learning.

AdamW is float32, LR3e−5, betas (.9,.999), epsilon 1e−8, weight decay 1e−4 and clip threshold 1. A finite but explosive Tiny K2 loss at step 38,443 motivated a recorded prospective K2 removal, retaining weights and moments. CC excluded K2 from the outset. Tiny moved from CPU to MPS at step 46,140 under a resource change. Prior, batch, conditioning and device changes form a bundle; no isolated cause or matched training-speed benefit is established.

Validation and confirmation banks were locked before training, with roots **6,000,000,000,000 / 7,000,000,000,000** and **368 / 736** functions. Confirmation has 128 functions per track except unseen dimensions (96), nested K4/8/16/32/64 and independent query rows. Main D4/8/16/32 and withheld D6/12/24 are separated. All saved 8K→64K checkpoints shown in the current learning figure are evaluated on this same new confirmation bank. They are not scores spliced from historical banks. Evaluations were recorded at 2K-step intervals.

The 32K→64K effects use **2,000 paired whole-function bootstrap resamples**, stratified by D/family and retaining nested K, seed **913867**. Intervals are exploratory and unadjusted. They condition on one selected pretrained trajectory per architecture and do not establish multi-seed continuation robustness.

Diabetes progression adds one D10 real dataset with disjoint train/validation/test roles; Facebook, Liver and SML2010 are reused guardrails. Each real task has eight support draws on fixed query rows over K4/8/16/32/64. The public point table is descriptive, without invented intervals. No real labels trained shared weights or selected checkpoints. Different draws of one dataset are not independent dataset-level replication.

## Current TabArena-Lite regression protocol

The official [TabArena](https://github.com/autogluon/tabarena) Lite regression task list contains 13 datasets. Each model uses one fixed completed 64K configuration and the official **repeat 0 / fold 0 / sample 0** outer split, with the runner's **8 inner folds × 1 set** and full-training refit. There is no neural HPO or task-time shared-weight optimization. Test labels enter scoring only.

All original columns and all official training/test rows are retained. Support-only numerical imputation/scaling and train-only categorical codes preserve original feature count; missing/unseen/known category codes are 0/1/2+. The two models share all nine support input fingerprints (eight inner folds plus full refit), targets and row order. Native metadata/feature tags can differ. D1024 QSAR-TID-11 and D81 superconductivity exceed the unchanged 32-feature capacity; they remain reported as unsupported, with no substituted scores.

The exact native-equation executor uses full support context beyond the original K64 API guard. For CC, attention includes every support key, with independent query tiling and cached projections only. Preflight native equivalence, finite K96, unchanged weights and query-batch independence were checked. Support counts are far beyond the synthetic training range. This changes the execution envelope without retraining or changing architecture equations.

Baseline RMSEs come from **published fixed configurations**, aligned to the same official task/split and 8×1 protocol, rather than new local baseline runs:

| Baseline | Published configuration | Artifact suite | Published compute |
| --- | --- | --- | --- |
| TabPFN 3.5 | `TabPFN-3.5_c1_default_BAG_L1` | `tabarena-2026-09-17-fix` | GPU |
| CatBoost | `CatBoost_c1_default_BAG_L1` | `tabarena-2026-07-13` | CPU |
| XGBoost | `XGBoost_c1_BAG_L1` | `tabarena-2025-06-12` | CPU |

Baselines have different internal preprocessing, implementations, pretraining and compute budgets. The selected published XGBoost scores are not imputed. These controls support conditional accuracy comparisons, not matched training-cost or commercial claims.

Within each dataset, RMSE is in the target's units. Across the **11 common datasets**, report `exp(mean(log(candidate_RMSE/reference_RMSE)))`; gap is `100 × (ratio − 1)`. Each dataset receives equal weight. Raw RMSEs across incompatible target units are not averaged. No confidence interval, official leaderboard rank or estimated leaderboard rank is inferred from this one-outer-split fixed-checkpoint comparison. CC ran on MPS with four host threads, while Tiny used CPU/one thread during concurrent research work; these timings cannot establish a matched speed comparison.

## Planned 64K→100K failure-driven regression

This is a future research direction, not an executed protocol or result. Use separate development datasets to turn observed failure categories into regression tasks, evaluate every **2K optimizer steps**, and declare checkpoint/stopping criteria before the next run. Already inspected TabArena-Lite tests cannot become an untouched confirmation set. Reserve fresh datasets/splits for subsequent confirmation, and monitor synthetic retention and real transfer jointly. No training or architecture change is performed for this documentation update.

## Mechanism attribution

The strongest mechanism test compares a candidate to a separately trained control with matched data, capacity and neural operations. Current-reader controls retain ordinary task-weight memory and substitute current pairs only for the added history read.

Frozen interventions answer a narrower question: whether the trained system depends on a component or evidence pairing. History-off removes the added residual; history-wrong-labels corrupts stored old pairings while keeping the current pair correct; freeze-hidden removes A/b updates. Shuffled labels break support correspondence, and reverse-order reverses both inputs and labels. These can disrupt co-adaptation or induce distribution shifts. They do not by themselves prove abstract concept reuse or identify a unique bottleneck.

Support interpolation and independent-query performance are reported separately. External gradient/solver diagnostics are labeled as diagnostics and are never presented as native TinyMind adaptation.

## Uncertainty

Historical plateau/fresh-experience intervals use **5,000 paired whole-function bootstrap replicates**, stratified by family/dimension and preserving each K curve. The matched Transformer study uses **10,000** such replicates. Seeds are reported separately, rather than pooled into an ensemble. Intervals condition on these generators and pretrained parents, not the population of possible training seeds. Exploratory subgroup intervals are unadjusted for multiple comparisons.

Beijing intervals use **10,000 whole-station resamples**, retaining four episodes and each K curve. Nearby stations are geographically dependent. Other real-study intervals condition on the fixed dataset/query sets and support draws, which are not independent datasets.

## Efficiency

The matched Transformer study uses Apple M4 CPU/float32, two threads, batch eight and 64 queries per function/support budget. Timings are single-pass amortized observations, not serving quantiles. Inference MACs cover the whole evaluated bank. Maximum task-cache bytes cover the D/K grid and exclude shared weights and runtime overhead. Forward MACs omit some pointwise work and all backward/optimizer work; they are not complete FLOPs or dollar estimates.

Beijing uses batch one, two threads and workload Q1/8/64/512/4096. Timings average a preselected eight-station hardware subset and include preprocessing/adaptation, excluding startup/service costs. Corrected numerical storage removes a 256-byte metadata alias double count in CC/Transformer states. Different experiments' timing tables are not mixed into matched comparisons.

## Evidence boundaries

The repository contains whitelisted aggregate tables, sanitized descriptions and source hashes. [Study cards](../benchmarks/results.md) bind numbers to benchmark, baseline, seed, metric and conditions. [Reproducibility](../reproducibility/README.md) distinguishes aggregate arithmetic checks from full predictive replication. Ongoing, unaudited experiments are excluded. No new training was performed to build this showcase.
