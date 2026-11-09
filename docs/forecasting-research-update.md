# Research update: from tabular experiments to forecasting

Evidence date: **5 November 2026**.

This study card retains the original pilot. [The 9 November update](current-research-2026-11-09.md) covers the current forecasting model and its latest measured results.

## Why we parked tabular development

We have **parked active tabular-model development and pivoted our current research toward time-series forecasting with persistent experience adaptation**. Tabular experiments produced some local and synthetic gains, but did not deliver the consistent, competitive real-world improvement we were seeking. The earlier TabArena-Lite comparison retained large accuracy gaps and unsupported high-dimensional cases. The later six-dataset improvement was narrower and did not establish general TabArena competitiveness.

Those historical successes and failures remain visible. The pivot does not erase their evidence or prove that every version of the architecture failed.

Forecasting supplies a natural causal experience stream: predict future observations, receive their outcomes later, update stream-local memory, and predict subsequent windows. We ask whether that experience improves unseen future predictions while shared neural weights stay frozen during deployment.

## Mechanism at a conceptual level

The system combines a compact recurrent forecasting core with experience-dependent residual memory:

1. The shared core supplies a base forecast from available rolling history.
2. Learned features represent the current forecasting situation.
3. Already arrived observations supply residual evidence to per-stream memory.
4. A learned policy controls evidence weighting and confidence in the memory correction.
5. Prediction combines the base forecast and the experience-dependent correction.

~~~mermaid
flowchart LR
    H[Available causal history] --> F[Shared forecasting core]
    F --> B[Base forecast]
    F --> E[Learned feature representation]
    O[Already arrived observations] --> M[Persistent per-stream residual memory]
    E --> M
    M --> C[Confidence-controlled correction]
    E --> C
    B --> P[Next prediction]
    C --> P
~~~

Shared weights stay frozen during online evaluation. Memory changes as labeled observations arrive, has separate state per stream, and can be saved and reloaded. Rolling history continues to supply recent information; persistence is not a claim that predictions require no context. Regularized residual-memory controls provide a non-learned alternative against which to test the learned policy.

## Completed forecasting pilot

We evaluated **12 selected short-horizon GIFT configurations** with **13,952 original forecast origins per method**, original splits and horizons. Five paired methods share the same rolling inputs. Training used synthetic streams; real benchmark examples, labels, predictions and evaluation feedback were excluded from outer optimization.

During evaluation, an earlier forecast window's labels become available to memory only after that window has elapsed. Future query labels never update the state used to predict that query.

This is the selected pilot, **not the full 97-configuration GIFT leaderboard, fev or TabArena-Lite**. Stateful causal adaptation differs from published zero-shot protocols.

Positive geometric RMSE gap means worse; negative means better. Each configuration has equal weight. We use the geometric mean of per-configuration RMSE ratios, rather than averaging raw errors with incompatible target units. Results are one-seed descriptive estimates without confidence intervals.

| Experience-adapted forecaster versus | Geometric RMSE gap | Wins / losses |
|---|---:|---:|
| Paired frozen rolling forecaster | **−7.33%** | **12 / 0** |
| Fixed RLS on the same learned features | **−0.20%** | **6 / 6** |
| Fixed initial policy on the same learned features | −3.32% | 12 / 0 |
| Fixed NLMS on the same learned features | −9.85% | 10 / 2 |
| Seasonal naive | **+13.31%** | 5 / 7 |
| Published Toto Open Base 1.0 | −3.61% | **3 / 9** |
| Published Moirai-2 | +64.46% | 2 / 10 |
| Published Chronos-2 | +79.99% | 2 / 10 |
| Published TimesFM-3 | +88.18% | 1 / 11 |
| Published TiRex-2 | +89.59% | 2 / 10 |

The strongest positive result is improvement over our frozen baseline across every selected configuration. **The learned policy adds only a small aggregate benefit over fixed RLS.** The full gain cannot be attributed solely to a learned updater: learned features, rolling context and residual memory also contribute.

A favorable geometric aggregate versus Toto coexists with losses on nine configurations; it does not establish general superiority over Toto. Several other public models remain substantially stronger, and seasonal naive wins overall.

Published player scores are pinned reference rows, not new controlled reruns. Their pretraining data, hardware, parameter budgets and online information-use protocols differ. These are exploratory accuracy comparisons, not matched-resource evidence or commercial superiority.

### Every selected configuration

| GIFT configuration | Frozen RMSE | Experience RMSE | Diagnostic NMSE | Fixed RLS RMSE |
|---|---:|---:|---:|---:|
| ett1/H/short | 17.685 | 17.3223 | 1.35766 | 17.5236 |
| ett2/H/short | 13.9949 | 13.2247 | 1.55471 | 13.2035 |
| ett1/15T/short | 4.32406 | 3.63702 | 2.67373 | 3.54754 |
| ett2/15T/short | 3.66352 | 3.54702 | 3.26938e+09 | 3.58985 |
| jena_weather/H/short | 52.7065 | 45.7951 | 3.60315e+12 | 44.8185 |
| jena_weather/10T/short | 40.8654 | 38.1703 | 3.80471e+13 | 38.0671 |
| solar/H/short | 49.0759 | 48.298 | 1.25115 | 48.3397 |
| electricity/H/short | 3771 | 3640.57 | 8.3562e+12 | 3631.12 |
| bizitobs_service/10S/short | 266.479 | 230.935 | 6.96267e+14 | 235.619 |
| bizitobs_application/10S/short | 4334.89 | 3662.95 | 68.8599 | 3781.28 |
| bitbrains_fast_storage/H/short | 1734.24 | 1662 | 5.18956e+17 | 1644.63 |
| bitbrains_rnd/H/short | 1331.4 | 1309.54 | 6.92182e+14 | 1324.73 |

The full five-method table is in [forecasting-pilot.csv](../benchmarks/forecasting-pilot.csv). [Reference RMSE rows](../benchmarks/forecasting-reference-rmse.csv) include original public source URLs, and [exact comparisons](../benchmarks/forecasting-comparisons.csv) retain full precision.

Diagnostic NMSE averages variance-normalized query errors and can become extreme on nearly constant windows. Geometric RMSE gains do not imply improvement in every aggregate NMSE.

## Independent queries, persistence and forgetting

A separate synthetic evaluation used **256 held-out streams**, independent query noise and five controls. The experience method reduced geometric query RMSE by **3.86% on unseen instances** and **3.49% on unfamiliar relationship variants**, with **91 wins / 37 losses** in each condition.

The unfamiliar-variant condition's mean query NMSE improved from 1.30246 to 1.25979. Unseen-instance mean NMSE worsened from 1.49835 to 1.51041 despite its geometric RMSE improvement. These are distribution-specific outcomes, not arbitrary relationship discovery.

Observed-example fitting improved, but is reported separately from independent-query prediction. Query targets never entered the observation stream. Saved old-query features were probed after later experience, without re-encoding the old examples for those probes.

State save/reload checks reproduced predictions. This supports stored-state persistence, while forgetting resistance remains unresolved. When relationship A was followed by B and then A again, old-A query RMSE after B worsened by **0.63% for unseen instances** and **1.07% for unfamiliar variants**. State retention does not prevent predictive interference.

[Independent-query aggregates](../benchmarks/forecasting-synthetic.csv) and [all retention controls](../benchmarks/forecasting-retention.csv) preserve favorable and unfavorable outcomes.

## Compute and evidence integrity

On the selected workload, shared rolling forwards took approximately 201.76 seconds; learned memory writes and reads added approximately 4.35 and 1.88 seconds. Their sum is about **3.09% additional component-processing time relative to shared forwards**, excluding download, startup, evaluation orchestration and service overhead.

This is a workload observation, not production latency or a competitor-speed comparison. [Exact component timings](../benchmarks/forecasting-timing.csv).

The retained audit independently rescored all **60 benchmark RMSE/NMSE rows**, **22,400 synthetic query rows** and **3,840 retention rows**. It checked causal label availability, benchmark truths against the preserved reference, shared-weight preservation and state reload behavior.

The verification scripts check arithmetic and integrity. They do not replay neural inference or the underlying saved-prediction audits. An audited internal result is not independent external replication.

## Next research questions

This pilot justifies further controlled research on persistent residual adaptation. It does not establish a state-of-the-art foundation model, universal continual learning, forgetting prevention or deployment readiness.

Priorities are repeatable benefit beyond fixed rules, a newly reserved confirmation suite after development, repeated seeds, broader temporal/dependency coverage, long-horizon and covariate validation, and a complete benchmark protocol with transparent online-adaptation classification.

Later completed forecasting experiments are documented in the dated update above, with their own controls and limitations.

[Forecasting provenance](../benchmarks/forecasting-provenance.json) · [Verification](../reproducibility/README.md) · [Historical tabular evidence](../benchmarks/results.md)
