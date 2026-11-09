# Earlier research

**Tabular research, including TinyMind-CC / ColumnContext, is stopped.** The follow-up failed to deliver competitive performance on the evaluated regression tasks. The active showcase is the [current forecasting model](../README.md).

[Earlier public research snapshot](archive/tinymind-through-2026-11-05.md) · [Historical architectures](architecture.md) · [Original forecasting pilot](forecasting-research-update.md)

## Archived CC continuation through 150K — stopped


The follow-up CC trajectory completed 150,000 cumulative updates in one original model seed. All ten reported checkpoints, including the starting reference, scored **13/13** official regression datasets using the existing **r0f0s0 outer split, eight inner folds and full-training refit**. Every original support row and feature is retained, including the previously unsupported high-dimensional datasets. This later coverage does not change the historical 64K model's 11/13 result.

| CC checkpoint | Geometric RMSE change vs 133,594 | Dataset wins / losses vs 133,594 | Macro NMSE |
|---:|---:|---:|---:|
| 133,594 | +0.000% | 0 / 0 | 0.424043 |
| 135,000 | +0.143% | 9 / 4 | 0.425151 |
| 137,000 | +1.940% | 4 / 9 | 0.432161 |
| 139,000 | +0.752% | 5 / 8 | 0.425812 |
| 141,000 | +0.975% | 6 / 7 | 0.429565 |
| 143,000 | +1.264% | 4 / 9 | 0.433012 |
| 145,000 | +0.028% | 8 / 5 | 0.423028 |
| 147,000 | −0.524% | 8 / 5 | 0.421121 |
| 149,000 | +0.695% | 4 / 9 | 0.431562 |
| 150,000 | +0.714% | 6 / 7 | 0.430810 |

The starting checkpoint compared with itself has thirteen ties. Dataset win counts do not determine the geometric aggregate. The best inspected milestone is 147K; the final 150K state is **0.714% worse** than the starting reference. More training did not deliver sustained improvement on this suite.

At 150K, geometric RMSE is **75.71% higher than published TabPFN 3.5**, **56.84% higher than CatBoost**, **52.73% higher than XGBoost**, and **45.34% higher than Random Forest**, with zero wins on the thirteen datasets against each. Earlier TabPFN versions are also retained in the tables.

These are local fixed-split results on previously evaluated datasets, with one neural seed and no confidence intervals. Published baseline defaults use different software and hardware and were not retrained here. This establishes neither an official leaderboard rank nor commercial superiority. The earlier six-dataset 70K gain remains a separate historical result.

[All dataset/checkpoint/reference scores](../benchmarks/current-tabarena-results.csv) · [Every milestone and baseline comparison](../benchmarks/current-tabarena-summary.csv)

## Other archived forecasting experiments

A separate phase-transport prototype failed its synthetic acceptance conditions: 2,357 of 6,174 checks failed. Seasonal amplitude collapse persisted despite small error changes. This prototype is separate from the current forecasting model's results.
