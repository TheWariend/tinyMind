# TinyMind

### Learning and adapting from experience, at approximately one million parameters

TinyMind is a research project studying how a compact neural system can use observed examples to change its predictions. We investigate two routes: **learned updates to task-specific neural weights** and **compressed, example-conditioned attention**.

**Current validated experiments predominantly concern numerical function learning and scalar regression.** The wider aim is learning from experience; language, agent learning, arbitrary relationship discovery and general intelligence are outside the demonstrated scope.

This public repository shares audited aggregate results, methodology and figures. Model implementations, weights and private research assets remain private. Evidence cutoff: **2 November 2026**.

[Architecture](docs/architecture.md) · [Research progress](docs/research-progress.md) · [Benchmarks](benchmarks/results.md) · [Methodology](docs/methodology.md) · [Limitations](docs/limitations.md) · [Reproducibility](reproducibility/README.md)

## The research question

Can a small, pretrained neural system learn useful relationships from a short sequence of input/outcome pairs while its shared weights stay frozen? Can that adaptation use earlier evidence, improve independent predictions and eventually transfer to genuinely unfamiliar relationships?

We separate **within-task adaptation** as observations arrive from **pretraining progress** across many tasks. More examples can improve an individual task even when longer pretraining has stopped improving held-out error.

## Two architectures, two forms of task memory

![TinyMind and ColumnContext architecture overview](figures/architecture.svg)

| | TinyMind | TinyMind-CC / ColumnContext |
| --- | --- | --- |
| Shared parameters | **1,029,764** in the original D32-compatible model | **988,689** |
| Task memory | Four small neural hypotheses; learned updates to hidden/output weights and confidence | Target-conditioned column slots and cached support-row representations |
| Adaptation | Shared evidence/credit networks write task-local neural weights | Shared encoders and attention construct task-local context |
| Query behavior | Evaluate the small adapted hypotheses | Attend to compressed columns and cached rows |
| Research role | Study evidence-dependent neural weight adaptation | Study efficient contextual learning and the accuracy cost of compression |

Both exist because they test different ways of storing experience and spending computation. ColumnContext has faster cached adaptation in the historical matched CPU study; TinyMind has a much cheaper repeated query readout. ColumnContext's row cache still grows with the support count. Both architectures remain experimental.

**Tiny_Global** is a historical experimental TinyMind variant with **1,032,973 parameters**. It adds learned historical retrieval and scalar ensemble-error feedback. It has demonstrated familiar-task benefits; it has **not** been promoted to the validated default. CC_D, CC_G and CC_DG are experimental training interventions on the unchanged ColumnContext architecture. See [checkpoint status](docs/architecture.md#checkpoint-status).

## Current evidence — completed 64K research endpoints

Both original architectures completed **64,000 cumulative optimizer steps** and **2,304,000 cumulative synthetic task presentations per model**. TinyMind has **1,029,764 parameters**; TinyMind-CC has **988,689**. The 32K→64K continuation added 32,000 steps at batch 64, or 2,048,000 presentations, to 256,000 earlier presentations. Presentations are not a count of unique mathematical functions.

![32K to 64K synthetic improvements and regressions](figures/pretraining-64k-effects.svg)

| Fixed 32K→64K comparison | TinyMind | TinyMind-CC |
| --- | ---: | ---: |
| Familiar NMSE reduction | **2.25%** | **4.77%** |
| Unseen-structure NMSE reduction | **−0.74%** (regression) | **6.66%** |
| Unseen-dimensional NMSE reduction | 2.57% | 4.36% |
| Expanded-robustness NMSE reduction | 0.31% (interval crosses zero) | −3.55% (interval crosses zero) |

These are fixed endpoint comparisons on the same locked confirmation bank, with one validation-selected parent per architecture: TinyMind seed **1877**, CC seed **1811**. The familiar and structure intervals exclude zero; all six tracks and exploratory 95% whole-function intervals are retained in [the 64K study card](benchmarks/results.md#current-32k64k-pretraining). Changes to prior, batch size and numerical conditioning make this a continuation bundle, rather than an isolated compute or architecture effect.

![Later pretraining learning curves on one confirmation bank](figures/pretraining-64k-curves.svg)

The earlier **4K–8K plateau was not a permanent training ceiling**. Subsequent 8K→32K and 32K→64K experiments produced further improvements. This does not establish uniform generalization or guarantee future gains; TinyMind's unseen-structure regression remains part of the current evidence.

### TabArena-Lite regression: coverage and remaining accuracy gap

![Relative RMSE on the 11 common TabArena-Lite datasets](figures/tabarena-lite-64k.svg)

| Current benchmark finding | Result |
| --- | --- |
| Coverage | **11/13 datasets for each model**; QSAR-TID-11 (D1024) and superconductivity (D81) exceed the unchanged 32-feature limit |
| TinyMind versus CC | TinyMind wins **8/11**; CC wins **3/11**; no ties |
| Geometric-mean relative RMSE gap versus TabPFN 3.5 | TinyMind **+69.63%**; CC **+84.66%** (positive gap is worse) |
| Wins versus published TabPFN 3.5, CatBoost or XGBoost | **0/11 for either model against each baseline** |

The comparison uses fixed 64K weights, official Lite regression splits (repeat 0/fold 0/sample 0), the 8×1 inner protocol and full original features/training supports. Baseline scores are published fixed-configuration results on aligned splits, rather than new local reruns. **No official TabArena rank or commercial superiority is established.** [All 13 dataset results and protocol limits](benchmarks/results.md#current-tabarena-lite-regression-at-64k).

Real-world accuracy remains inconsistent despite the synthetic improvements. The 64K small-support study also has gains and regressions across Diabetes, Facebook, Liver and SML2010. These conditional results and the older Beijing findings are preserved in [the benchmark report](benchmarks/results.md).

## Historical evidence — through 1 November 2026

The following results retain their original checkpoints, banks and controls. They describe earlier studies, rather than the current 64K endpoints.

### What the earlier evidence supports

| Evidence category | Finding | Scope |
| --- | --- | --- |
| **Validated finding** | Both prototypes learn useful predictions from observed examples with shared weights frozen | Predominantly controlled numerical regression; independent query evaluation |
| **Experimental finding** | Tiny_Global reduces familiar all-K error by **2.34% / 2.06%** versus the strongest declared matched controls | Seeds 1811 / 1877, final bank, 8K checkpoints, K4/8/16/32/64 |
| **Experimental finding** | Its familiar K16/32/64 reduction is **5.27% / 5.00%** | Same benchmark and controls; a secondary support-size endpoint |
| **Frozen causal diagnostic** | Corrupting historical pairings, disabling new retrieval or freezing hidden updates worsens familiar predictions | Same experimental weights, development bank; intervention effects do not prove arbitrary rule invention |
| **Validated comparison** | ColumnContext uses **7.48× less inference MAC work** and **26.24× less maximum task-cache storage** than the tested Transformer | Matched data/step recipe; measured CPU study; Transformer has better all-K nonlinear accuracy |
| **Unsuccessful hypothesis** | Fresh experience, several learning-mechanism changes and the 1 November repairs did not overcome the broad 4K plateau in those studies | Bounded 4K–8K studies; their gated 10K/12K extensions were not run; later original-architecture training progressed to 64K |

### Familiar gains, unresolved unfamiliar transfer

![Matched final effects with paired confidence intervals](figures/matched-effects.svg)

Tiny_Global versus **Tiny_Basis_current**, final query NMSE; lower is better. Intervals are paired 95% whole-function bootstrap intervals.

| Seed | Benchmark | Control NMSE | Tiny_Global NMSE | Error reduction [95% CI] |
| --- | --- | ---: | ---: | --- |
| 1811 | Familiar, all K | 0.682809 | 0.666817 | **2.34% [1.99, 2.70]** |
| 1877 | Familiar, all K | 0.676726 | 0.662791 | **2.06% [1.69, 2.45]** |
| 1811 | Familiar, K16/32/64 | 0.480355 | 0.455022 | **5.27% [4.65, 5.93]** |
| 1877 | Familiar, K16/32/64 | 0.473873 | 0.450167 | **5.00% [4.38, 5.69]** |
| 1811 | Excluded programs, all K | 0.895739 | 0.894178 | 0.17% [−0.35, 0.72] |
| 1877 | Excluded programs, all K | 0.893749 | 0.896406 | −0.30% [−0.81, 0.25] |

The excluded-program intervals cross zero in both seeds. **Generalization to arbitrary unfamiliar relationships remains unsolved.** Complete, full-precision results and alternate matched controls are in [public-results.csv](benchmarks/public-results.csv); the exact study conditions are in [results.md](benchmarks/results.md).

### Efficiency comes with an accuracy tradeoff

![ColumnContext and Transformer efficiency and accuracy comparison](figures/efficiency.svg)

The conventional **994,945-parameter axial Transformer** reduces nonlinear all-K error by **2.33% / 5.33% relative to ColumnContext** in seeds 1301 / 1337. ColumnContext retains large measured compute and cache advantages. This comparison matches training data, steps and optimizer settings; compute, architectural components and initialization differ. It establishes a tradeoff under this recipe, not a uniform architecture winner.

### Pretraining progress and its limits

![Original training improves early and plateaus after 4K](figures/original-pretraining.svg)

Early pretraining improves held-out familiar prediction. Extending the original fresh-experience arms from 4K to 8K yields only **0.70% / 0.52%** familiar reductions for TinyMind and **−0.14% / 0.83%** for CC on that study's bank. The historical 1 November repair study also fails its full gates; later original-architecture continuations made additional progress. [Progress and failed experiments](docs/research-progress.md) includes the complete chronology and [repair curves](figures/plateau-repair.svg).

### Real-world results are mixed

![Chronological Beijing air-quality evaluation](figures/real-world.svg)

On a chronological, 24-hour-ahead PM2.5 test across twelve Beijing stations, CC's K64 NMSE is **0.780720 / 0.830184**, versus **0.825067** for persistence. Its advantage over persistence is statistically uncertain. TinyMind's validated default scores **1.031620** and loses to KNN5 (**0.840694**). Persistence is stronger at smaller support sizes and much cheaper. Four additional, previously studied regression datasets provide conditional evidence with documented development/final row overlap. [Full real-world results and caveats](benchmarks/results.md#real-world-evaluation).

## What remains unsolved

- Reliable acquisition of genuinely unfamiliar relationships and reusable cross-task concepts.
- Consistent, sustained pretraining progress across synthetic tracks and real-world tasks.
- Consistent accuracy across dimensions, support sizes, families and real datasets.
- Retention without prediction drift, reliable uncertainty and deployment robustness.
- Independent replication and broader application validation.

Our evidence does not identify a unique capacity, optimization or credit-assignment cause. Lower support fitting error alone is insufficient: some diagnostic interventions improve interpolation while worsening independent predictions. See [limitations](docs/limitations.md).

## Research roadmap

| Phase | Status | Milestone |
| --- | --- | --- |
| **1. Architecture research** | Prototypes completed | Working TinyMind and ColumnContext numerical-regression systems |
| **2. Learning mechanisms** | Partial evidence; ongoing | Evidence-dependent adaptation and useful historical retrieval; credit assignment and retention blockers remain |
| **3. Generalization** | Open | Consistent improvement on genuinely unfamiliar relationships, beyond supplied primitives |
| **4. Sustained pretraining** | Further progress demonstrated through 64K; next test planned | 64K→100K failure-driven regression training, separate development datasets and evaluations every 2K steps |
| **5. Independent validation** | Initial Lite comparison completed; external replication open | Wider untouched benchmarks, reliability and deployment evaluation |

The next research direction is **64K→100K failure-driven regression training**. Failures will guide a separate development suite, with 2K-step evaluations and predeclared safeguards. It is a planned experiment, with no 100K result yet. The known TabArena-Lite test outcomes are not a fresh development or untouched confirmation set. This documentation update launches no training and changes no model architecture.

## Inspect the evidence

Every numerical chart is generated from public aggregate tables. [Provenance](benchmarks/provenance.json) records private source identifiers and SHA256 hashes; [figure sources](figures/README.md) map each chart to its public inputs. Public scripts verify the exported arithmetic and regenerate numerical figures. Full training or inference reproduction requires assets withheld from this showcase.

No model weights, private model source, raw datasets, development logs or software reuse license are distributed here. Licensing for any future implementation or model release requires a separate decision.
