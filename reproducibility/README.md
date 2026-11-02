# Reproducibility

This release supports inspection of aggregate evidence, verification of percentage arithmetic and regeneration of numerical figures. It withholds the private model implementation, checkpoints, optimizer states, training/evaluation banks, raw real data and development logs.

## Verify the public export

From the repository root, with Python 3:

```sh
python3 reproducibility/verify_results.py
```

The standard-library script verifies every published CSV hash and row count, finite metrics, comparison arithmetic, interval ordering where intervals are reported, unique result identifiers and local documentation/figure links. It also checks 64K exposure accounting, endpoint/curve agreement, TabArena coverage, pairwise wins and geometric-mean RMSE ratios. It performs no model evaluation or training.

Every row of [public-results.csv](../benchmarks/public-results.csv) identifies its study, split, candidate, reference, seed, metric, support/dimension conditions, paired unit count and exact source locator. [provenance.json](../benchmarks/provenance.json) stores hashes of the original private evidence artifacts and public CSVs. Private relative artifact identifiers are provenance labels, not public download links.

Rows with **bootstrap_replicates=0** and blank CI fields are explicitly descriptive: the current all-K real point comparisons and fixed-checkpoint TabArena dataset/ratio comparisons. Their paired unit count describes support draws, scored test rows or common datasets, as specified in the study card; it does not imply independent replications. The normalized reference value 1 in geometric-mean rows is a ratio reference, not a raw target-unit RMSE.

The prior 431 comparisons and eight historical source CSVs are preserved. Current evidence adds six whitelisted aggregate tables, without predictions, observations or raw labels. `as_of` and added source hashes distinguish the 2 November evidence from the pinned 1 November export.

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
| Binding to retained private evidence | Source SHA256 hashes and exact locators available |
| Bootstrap confidence interval regeneration | Unsupported from aggregates alone; audited intervals preserved |
| Saved prediction→NMSE recomputation | Performed in the private audit; predictions/targets withheld |
| Neural inference or training-from-scratch | Requires private implementation, weights, banks and original environment |

The historical 1 November private plateau audit recomputed **643,040 neural** and **23,560 classical** score rows from saved predictions, with maximum NMSE discrepancy **2.14×10⁻¹⁴** after rounding upward. It verified protected artifacts and evaluation integrity. These are retained audit observations, not an independent external replication performed by this repository.

The current 64K audit recomputed **276,800 score rows**, with maximum NMSE discrepancy **2.14×10⁻¹⁴** after rounding upward. Optimizer counters, completed intervals, exposure totals and protected artifacts passed the retained audit. The separate TabArena verification recomputed **64,120 saved test predictions per model**, checked all 13 coverage outcomes, all nine shared support fingerprints, aligned outer/inner splits, preserved states and zero neural optimization. Sanitized audit fields and original source hashes are in [provenance](../benchmarks/provenance.json).

These public scripts check aggregate consistency; they cannot independently reproduce the private audits or rerun the official TabArena evaluator. Baseline results are the retained published configurations, not newly executed local baseline inference. No 100K run is included.

Publishing figures and aggregates does not imply that a private training ZIP, runtime or dataset is cleared for distribution. No executable model evaluation example or software reuse license is included. A future replication release needs explicit decisions about source, checkpoints, dataset permissions and licensing.
