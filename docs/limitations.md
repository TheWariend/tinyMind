# Limitations and open questions

TinyMind is a numerical-regression research program with useful compact-learning observations. **Arbitrary unfamiliar relationship generalization has not been solved.** No model in this release is certified for deployment, general intelligence, language learning or autonomous agent learning.

## Experimental coverage

- Two continuation seeds inherit specific pretrained parents. Paired bootstrap intervals do not establish robustness across all training seeds.
- Most synthetic tests use D4/8/16/32 and K≤64. Larger-support gains mean tested K16/32/64, not extrapolation beyond the architecture's bound.
- Held-out generating programs contain some familiar primitives. Their scores do not prove new mathematical concepts or compositional invention.
- Generator distributions, curricula and supplied Fourier/polynomial encodings affect results. Some generators normalize the full function pool before supports are selected.
- Independent queries matter, but support-fitting and causal corruption diagnostics answer narrower questions. Their effects do not uniquely identify abstract learning, retention or a plateau cause.

## Generalization, memory and plateau

Tiny_Global's familiar gains are reproducible against matched readers; its strongest-control excluded intervals cross zero in both seeds. Original and improved 6K→8K gains are small. CC's broad data/clipping repairs fail even though one simple Fourier subgroup improves.

No 10K/12K continuation was run after the failed gates. Missing endpoints cannot be interpreted as zero error or projected improvements. No experimental checkpoint was promoted.

More observations can improve query prediction while earlier support predictions drift. The evidence does not separate all sample-specific fitting from knowledge damage or establish loss-free retention. Historical retrieval is bounded; persistent reusable concepts across tasks remain untested.

## Real-world evidence

The Beijing test has one dataset, twelve nearby stations and four periods. Stations are geographically dependent. Increasing K adds more recent calibration information as well as more evidence. Support count and recency are confounded. CC's advantage over persistence is uncertain; TinyMind loses to KNN. All tested simple baselines are cheaper in total cost within the measured Q1–4096 workloads.

The plateau pilot's Facebook, Liver, SML2010 and temperature tasks use previously studied datasets. Each task has disjoint supports/queries, but development/final query overlap is **34/128**, **35/113**, **21/128** and **10/128** rows respectively. Additionally, 69 Facebook and 74 Liver final-query rows appeared in development supports. These are conditional support/split-draw confirmations rather than fully reserved query-row or untouched dataset-level validation. No real labels train the shared neural weights.

SML2010 is same-time dining sensor regression, not future forecasting. The temperature task uses current observations and already-issued forecasts. Dataset scope, missing-value treatment, chronological splits and feature construction are supplied protocol choices.

## Comparisons and efficiency

The matched Transformer study equalizes data, steps and optimizer settings; it does not equalize compute, architectural embeddings or initialization. ColumnContext's efficiency benefit coexists with worse all-K nonlinear accuracy. Historical Tiny defaults, replay variants and Transformer references in other studies have unmatched training lineage.

CPU timings are observations on Apple M4 under stated thread/batch settings, not production tail latency. Forward MACs are incomplete operator accounting; cache payloads exclude runtime/container overhead and shared weights. Results do not imply GPU savings, energy savings, hosting prices or commercial advantage. Batch-amortized per-query times are not standalone single-query latencies.

## Reproducibility limits

Public aggregates permit arithmetic checks and figure regeneration. They cannot regenerate per-function bootstrap samples, replay neural inference or reproduce pretraining without private source, weights and task banks. Provenance hashes bind the export to retained artifacts, but withheld sources cannot be independently downloaded from this repository.

External replication, calibration, uncertainty reliability, distribution-shift robustness, broader applications and deployment testing remain open. Any later public implementation or model release requires an explicit licensing and asset decision.
