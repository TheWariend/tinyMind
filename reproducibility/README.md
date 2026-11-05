# Reproducibility

The verification tools check aggregate evidence, percentage arithmetic and numerical figures.

## Verify the public export

From the repository root, with Python 3:

```sh
python3 reproducibility/verify_results.py
```

The standard-library script verifies every published CSV hash and row count, finite metrics, comparison arithmetic, interval ordering where intervals are reported, unique result identifiers and local documentation/figure links. It also checks earlier 64K exposure accounting, endpoint/curve agreement and TabArena coverage, plus the latest six-dataset 70K endpoint/ML comparisons and geometric-mean ratios. It performs no model evaluation or training.

The 5 November forecasting addition has its own [provenance manifest](../benchmarks/forecasting-provenance.json) and six aggregate exports. The verifier checks all 60 five-method RMSE/NMSE rows, 84 reference rows, 11 geometric RMSE comparisons, query/retention summary integrity and component-timing arithmetic.

Independent query and retention summaries are bound to retained audits. Public aggregate checks do not reproduce the underlying saved-prediction audits or neural inference.

Every row of [public-results.csv](../benchmarks/public-results.csv) identifies its study, split, candidate, reference, seed, metric, support/dimension conditions, paired unit count and exact source locator. [provenance.json](../benchmarks/provenance.json) stores hashes of the original evidence and CSVs. Artifact identifiers are provenance labels, not download links.

Rows with **bootstrap_replicates=0** and blank CI fields are explicitly descriptive: the earlier 64K all-K real point comparisons and fixed-checkpoint TabArena dataset/ratio comparisons. Their paired unit count describes support draws, scored test rows or common datasets, as specified in the study card; it does not imply independent replications. The normalized reference value 1 in geometric-mean rows is a ratio reference, not a raw target-unit RMSE.

The prior 431 comparisons and eight historical source CSVs are preserved. The earlier 64K update added six aggregate tables. `as_of` and added source hashes distinguish the 2 November evidence from the pinned 1 November export.

The latest six-dataset export adds two aggregate CSVs and 56 descriptive comparisons. Existing 533 comparisons and previous source tables remain unchanged. Provenance uses evidence labels and retained SHA256 hashes. Zero bootstrap replicates and blank interval fields indicate the absence of confidence intervals.

The six-dataset verification independently checks CC's 9.61% RMSE reduction, TinyMind's nominal regression, the validation-selected steps, dataset-level regressions and both matched-support/full-training tree baseline regimes. These results are separate from TabArena-Lite; no unavailable TabPFN score is inserted.

## Regenerate numerical figures

Install Matplotlib in your preferred Python environment, then run:

```sh
python3 reproducibility/render_figures.py
```

The renderer reads only public CSV files and writes SVGs in `figures/`. It regenerates all numerical charts; the architecture diagram is an authored explanatory SVG. Original rendering used Matplotlib 3.11.2. Matplotlib 3.x is sufficient for the script, though font/rendering differences may change SVG bytes. Fonts are embedded as paths; SVG metadata contains no local source paths.

## What can be independently checked?

| Check | Public release support |
| --- | --- |
| Reported point errors and percentage reductions | Exact aggregate inputs and arithmetic available |
| Chart data, labels, scope and failures | Public tables and renderer available |
| Binding to retained evidence | Source SHA256 hashes and exact locators available |
| Bootstrap confidence interval regeneration | Unsupported from aggregates alone; audited intervals preserved |
| Saved prediction→NMSE recomputation | Performed in the retained audit; not rerun by aggregate verification |
| Neural inference or training-from-scratch | Not executed by the aggregate verification tools |

The historical 1 November plateau audit recomputed **643,040 neural** and **23,560 classical** score rows from saved predictions, with maximum NMSE discrepancy **2.14×10⁻¹⁴** after rounding upward. It verified protected artifacts and evaluation integrity. These are retained audit observations, not an independent external replication performed by this repository.

The earlier 64K audit recomputed **276,800 score rows**, with maximum NMSE discrepancy **2.14×10⁻¹⁴** after rounding upward. Optimizer counters, completed intervals, exposure totals and protected artifacts passed the retained audit. The separate TabArena verification recomputed **64,120 saved test predictions per model**, checked all 13 coverage outcomes, all nine shared support fingerprints, aligned outer/inner splits, preserved states and zero neural optimization. Sanitized audit fields and original source hashes are in [provenance](../benchmarks/provenance.json).

These scripts check aggregate consistency; they do not replay the saved-prediction audits or rerun the official TabArena evaluator. The earlier 64K TabArena baselines are retained published scores. The latest six-dataset CatBoost/XGBoost scores were locally evaluated in the completed research campaign. No 100K run is included.

The latest retained audits verified selection before test scoring, matched support/test targets, preserved columns and no shared-weight updates during evaluation. They rescored 216 real prediction files and 24 baseline files and verified 12,000 completed continuation updates. Aggregate verification checks arithmetic and integrity; it does not replay inference or those audits.
