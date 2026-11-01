# Methodology

The experiments ask whether examples improve predictions on independent queries. Within-task adaptation, pretraining progress, mechanism attribution and real-world transfer are separate questions with separate controls.

## Common numerical-regression protocol

Each task provides ordinary input/outcome pairs. Query labels are withheld from adaptation. Shared weights stay frozen during evaluation; only task-local weights or context change. K curves use nested support prefixes, generally K4/8/16/32/64, disjoint from query rows. D4/8/16/32 is the main synthetic coverage; D6/12/24 is a withheld-dimensional track in later pilots.

Learner-side centering/scaling and imputation use supports only. Numerical scale is generally twice the population standard deviation, with a fallback of one for zero scales. Some synthetic generators center/scale the complete generated function pool as a **generative prior**. That is disclosed separately from learner normalization; these studies do not establish strictly streaming normalization.

The usual NMSE is each function's physical-unit mean query squared error divided by that function's query-target population variance, with a small floor where specified, then averaged under that study's declared family/dimension/support weighting. Reporting query variance never supplies query labels to the learner. Equal family weighting and occurrence weighting can differ across studies; study cards specify which estimate is shown.

Error reduction is `100 × (1 − candidate_error/reference_error)`. Positive favors the named candidate; negative is a regression. This is a percentage of **error**, not accuracy percentage points. The transformation is applied to aggregate errors, not averaged per-function percentage gains. Scientific comparisons never combine errors from different banks.

## Latest original-lineage plateau repair

Seeds **1811 and 1877** restore original fresh-experience 4K weights and AdamW moments. Twenty separately trained continuations each add 4,000 steps (80,000 continuation optimizer steps in total), batch eight, ordinary normalized scalar query MSE. Original parameters use constant 3e−5 LR; new small Tiny credit/retrieval parameters and matched current readers use a declared 3e−4 group. AdamW uses betas (.9,.999), epsilon 1e−8 and weight decay 1e−4.

Arms share saved function occurrences, batch order, positions, feature tags and D/K schedule. CC distribution interventions alone replace roughly half the nonlinear occurrences with scaffolded laws. They test a **difficulty/composition bundle**, not isolated diversity, frequency or sparsity effects. Clipping-only arms change threshold 1→5.

Fresh development/final banks were generated and hash-locked before candidate training. The generator root is **1000013269457**, with development/final bank roots **1000113269457 / 1000213269457**; the final bank hash is in [provenance](../benchmarks/provenance.json). They contain **604 / 1,176** function/task draws, including real support draws. Familiar synthetic counts are 256 / 512; excluded 64 / 128; structural 32 / 64; unseen-D 96 / 192; controlled 124 / 248; each of four real datasets has eight draws. Original-prior families are affine, tanh-ridge, random neural and Fourier. Most synthetic tasks have 64 queries; some controlled cases have 128. Real counts are in the study card.

The primary endpoint is familiar **all K**. K16/32/64 is secondary. A common candidate could advance only if both seeds met all criteria: at least 5% all-K improvement over both strongest matched control and original 8K with positive intervals; at least 1% 6K→8K progress with positive intervals; excluded/structure/real safeguards and every-K familiar nonregression. **No candidate passed.** The nominal development-selected Tiny_Global and CC_G were reported on the independent final bank without final-driven reselection. No 10K/12K extension or promotion occurred.

## Mechanism attribution

The strongest mechanism test compares a candidate to a separately trained control with matched data, capacity and neural operations. Current-reader controls retain ordinary task-weight memory and substitute current pairs only for the added history read.

Frozen interventions answer a narrower question: whether the trained system depends on a component or evidence pairing. History-off removes the added residual; history-wrong-labels corrupts stored old pairings while keeping the current pair correct; freeze-hidden removes A/b updates. Shuffled labels break support correspondence, and reverse-order reverses both inputs and labels. These can disrupt co-adaptation or induce distribution shifts. They do not by themselves prove abstract concept reuse or identify a unique bottleneck.

Support interpolation and independent-query performance are reported separately. External gradient/solver diagnostics are labeled as diagnostics and are never presented as native TinyMind adaptation.

## Uncertainty

Plateau/fresh-experience intervals use **5,000 paired whole-function bootstrap replicates**, stratified by family/dimension and preserving each K curve. The matched Transformer study uses **10,000** such replicates. Seeds are reported separately, rather than pooled into an ensemble. Intervals condition on these generators and pretrained parents, not the population of possible training seeds. Exploratory subgroup intervals are unadjusted for multiple comparisons.

Beijing intervals use **10,000 whole-station resamples**, retaining four episodes and each K curve. Nearby stations are geographically dependent. Other real-study intervals condition on the fixed dataset/query sets and support draws, which are not independent datasets.

## Efficiency

The matched Transformer study uses Apple M4 CPU/float32, two threads, batch eight and 64 queries per function/support budget. Timings are single-pass amortized observations, not serving quantiles. Inference MACs cover the whole evaluated bank. Maximum task-cache bytes cover the D/K grid and exclude shared weights and runtime overhead. Forward MACs omit some pointwise work and all backward/optimizer work; they are not complete FLOPs or dollar estimates.

Beijing uses batch one, two threads and workload Q1/8/64/512/4096. Timings average a preselected eight-station hardware subset and include preprocessing/adaptation, excluding startup/service costs. Corrected numerical storage removes a 256-byte metadata alias double count in CC/Transformer states. Different experiments' timing tables are not mixed into matched comparisons.

## Evidence boundaries

The repository contains whitelisted aggregate tables, sanitized descriptions and source hashes. [Study cards](../benchmarks/results.md) bind numbers to benchmark, baseline, seed, metric and conditions. [Reproducibility](../reproducibility/README.md) distinguishes aggregate arithmetic checks from full predictive replication. Ongoing, unaudited experiments are excluded. No new training was performed to build this showcase.
