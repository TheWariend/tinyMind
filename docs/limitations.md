# Limitations and open questions

TinyMind is a numerical-regression research program with useful compact-learning observations. **Arbitrary unfamiliar relationship generalization has not been solved.** Both architectures remain experimental. No model in this release is certified for deployment, general intelligence, language learning or autonomous agent learning. No official TabArena rank or commercial superiority is established.

## Experimental coverage

- Historical repair experiments report two inherited-parent seeds. The current 32K→64K continuation has only one validation-selected parent per architecture (Tiny 1877, CC 1811). Paired bootstrap intervals do not establish robustness across training seeds or correct for parent selection.
- Most synthetic tests use D4/8/16/32 and K≤64. Historical larger-support gains mean K16/32/64. The current all-row TabArena executor goes beyond the original support admission guard; it does not expand the 32-feature capacity, and its supports are outside the synthetic training range.
- The current continuation changes prior, batch size and conditioning together, with a recorded Tiny K2 loss amendment and CPU/MPS resource change. It cannot isolate a pure compute, prior, numerical or architecture cause.
- Held-out generating programs contain some familiar primitives. Their scores do not prove new mathematical concepts or compositional invention.
- Generator distributions, curricula and supplied Fourier/polynomial encodings affect results. Some generators normalize the full function pool before supports are selected.
- Independent queries matter, but support-fitting and causal corruption diagnostics answer narrower questions. Their effects do not uniquely identify abstract learning, retention or a plateau cause.

## Generalization, memory and plateau

Tiny_Global's familiar gains are reproducible against matched readers; its strongest-control excluded intervals cross zero in both seeds. Original and improved 6K→8K gains are small. CC's broad data/clipping repairs fail even though one simple Fourier subgroup improves.

No gated 10K/12K extension was run in the historical plateau-repair study. Missing endpoints cannot be interpreted as zero error or projected improvements. Later, separately designed original-architecture runs reached 32K and 64K with additional improvements. The 4K–8K plateau was therefore not a permanent ceiling. No experimental checkpoint was promoted.

Current familiar NMSE gains of 2.25% / 4.77% coexist with a Tiny unseen-structure regression of 0.74%, versus a CC improvement of 6.66%. Tiny excluded-operation and both expanded-robustness intervals cross zero; CC expanded robustness nominally worsens 3.55%. Continued training is not uniformly beneficial. The planned 100K endpoint has no result yet.

More observations can improve query prediction while earlier support predictions drift. The evidence does not separate all sample-specific fitting from knowledge damage or establish loss-free retention. Historical retrieval is bounded; persistent reusable concepts across tasks remain untested.

## Real-world evidence

The Beijing test has one dataset, twelve nearby stations and four periods. Stations are geographically dependent. Increasing K adds more recent calibration information as well as more evidence. Support count and recency are confounded. CC's advantage over persistence is uncertain; TinyMind loses to KNN. All tested simple baselines are cheaper in total cost within the measured Q1–4096 workloads.

The plateau pilot's Facebook, Liver, SML2010 and temperature tasks use previously studied datasets. Each task has disjoint supports/queries, but development/final query overlap is **34/128**, **35/113**, **21/128** and **10/128** rows respectively. Additionally, 69 Facebook and 74 Liver final-query rows appeared in development supports. These are conditional support/split-draw confirmations rather than fully reserved query-row or untouched dataset-level validation. No real labels train the shared neural weights.

SML2010 is same-time dining sensor regression, not future forecasting. The temperature task uses current observations and already-issued forecasts. Dataset scope, missing-value treatment, chronological splits and feature construction are supplied protocol choices.

## Current TabArena-Lite and 64K real-data limits

Both models evaluated **11/13** Lite regression datasets. D1024 QSAR-TID-11 and D81 superconductivity remain unsupported; their absence is not a success or an imputed failure score. Geometric-mean RMSE gaps use only the 11 common datasets. TinyMind wins 8/11 pairwise versus CC, but **neither beats published TabPFN 3.5, CatBoost or XGBoost on any of those 11**. Gaps versus TabPFN 3.5 are **+69.63% / +84.66%**. Real-world accuracy remains inconsistent despite synthetic improvement.

This is one official outer split (repeat 0/fold 0/sample 0), with the 8×1 inner protocol, one fixed checkpoint/configuration per architecture and no reported intervals. Published baseline configurations share task/split scoring but differ in model internals, preprocessing, versions and compute. It is a local conditional comparison, not a complete official TabArena submission, leaderboard rank or proof of commercial superiority. Numerical executor equivalence in tested native cases does not validate arbitrary large-support generalization.

The small-support 64K real study adds one Diabetes dataset and reuses Facebook, Liver and SML2010 guardrails. Eight support draws share fixed query sets; their point gains/regressions are not eight independent datasets. Earlier exposure to guardrails limits untouched dataset-level claims. No real labels select or train the shared neural checkpoints.

Known benchmark failures can guide separate development tasks. If the inspected TabArena tests later influence task design or checkpoint choice, their subsequent scores cannot be presented as fresh untouched confirmation. The planned 64K→100K direction needs separately reserved development and confirmation evidence.

## Comparisons and efficiency

The matched Transformer study equalizes data, steps and optimizer settings; it does not equalize compute, architectural embeddings or initialization. ColumnContext's efficiency benefit coexists with worse all-K nonlinear accuracy. Historical Tiny defaults, replay variants and Transformer references in other studies have unmatched training lineage.

CPU timings are observations on Apple M4 under stated thread/batch settings, not production tail latency. Forward MACs are incomplete operator accounting; cache payloads exclude runtime/container overhead and shared weights. Results do not imply GPU savings, energy savings, hosting prices or commercial advantage. Batch-amortized per-query times are not standalone single-query latencies.

## Reproducibility limits

Public aggregates permit arithmetic checks and figure regeneration. They cannot regenerate per-function bootstrap samples, replay neural inference or reproduce pretraining without private source, weights and task banks. Provenance hashes bind the export to retained artifacts, but withheld sources cannot be independently downloaded from this repository.

External replication, calibration, uncertainty reliability, distribution-shift robustness, broader applications and deployment testing remain open. Any later public implementation or model release requires an explicit licensing and asset decision.
