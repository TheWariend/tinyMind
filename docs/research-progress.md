# Research progress

Evidence cutoff: **1 November 2026**. These milestones preserve both positive observations and rejected hypotheses. A failed gate does not erase a small gain; a small gain does not establish the wider goal.

## Phase 1 — Architecture research: prototypes completed

Working TinyMind weight-adaptation and ColumnContext attention prototypes are established in bounded numerical-regression experiments. TinyMind has cheap repeated predictions and compact task weights. ColumnContext compresses context and trades more query work/cache for faster adaptation. Validated TinyMind default11 remains unchanged; CC S4 is an unpromoted reference.

The 31 October matched Transformer study finds stronger all-K nonlinear accuracy for a conventional architecture, alongside substantial ColumnContext efficiency savings. This preserves an important control against attributing performance automatically to custom mechanisms.

## Phase 2 — Learning mechanisms: partial evidence, unresolved blockers

Observed pairs matter to the systems' predictions. The latest Tiny_Global history/feedback variant has reproducible familiar-query gains beyond separately trained current readers. Its own capacity-matched control yields 2.33% / 2.10% reductions; the strongest declared controls yield 2.34% / 2.06%. Added historical retrieval, hidden updates and correct historical pairings matter in frozen development diagnostics.

![Causal intervention effects](../figures/causal-evidence.svg)

This is progress in evidence-dependent familiar learning. Reliable excluded-program benefits over the strongest matched controls, retention guarantees and cross-task concept reuse remain open.

## Original pretraining and the 4K plateau

The controlled scaling study trained eight scratch arms to 8K. Familiar 1K→4K improvements range **5.5–17.8%** under changing source-to-mixed curricula. Familiar 4K→8K improvements are only **0.43–0.81%** on its own bank. These ranges describe that study's eight arms; they cannot be transferred to another bank or treated as a pure compute effect.

The subsequent fresh-experience study compares identical initialization/schedule with fixed-pool versus fresh function-and-observation coverage. Original fresh arms improve familiar error **10.60% / 10.42%** (Tiny) and **14.50% / 17.14%** (CC) from 1K to 4K. Their 4K→8K gains shrink to **0.70% / 0.52%** and **−0.14% / 0.83%**. Fresh-vs-fixed Tiny endpoint gains are 0.47% / 0.42%, while CC's effects are −0.33% / +0.83%. Fresh experience did not overcome the plateau under that schedule.

![Original pretraining](../figures/original-pretraining.svg)

## Latest 4K→8K repair: useful sub-results, broad gate failure

Twenty continuations from the two original 4K parents test native replication, dimension correction, Tiny history/feedback and CC data×clipping interventions. Original 8K parameters and historical predictions reproduce exactly in the saved-artifact audit.

Tiny_Global improves familiar final error by 2.34% / 2.06% versus the strongest declared matched controls and 5.27% / 5.00% at K16/32/64. Against original Tiny_R, gains are larger, **5.35% / 5.21%**, because that contrast bundles the correction and additional changes. Those larger numbers must not be presented as the isolated history effect.

![Independent final repair curves](../figures/plateau-repair.svg)

Progress from 6K to 8K remains small. CC's nominal selected clipping candidate regresses familiar all-K error by **0.36% / 0.50%**. No candidate passes the complete locked development gates; 10K/12K endpoints are **not run**, rather than zero or missing successes. The original default remains unchanged.

CC_D confirms a narrow **single-component Fourier** benefit at D4/K32–64: **15.50% / 13.03%**, with positive unadjusted intervals. Earlier development composition gains do not reliably replicate: final composition effects are **−2.61% / −9.98%**, with wide intervals crossing zero.

![Success and failure in the CC curriculum subgroups](../figures/curriculum-subgroups.svg)

## Unsuccessful hypotheses and what they leave open

| Hypothesis or intervention | Observed outcome | Interpretation |
| --- | --- | --- |
| More fresh functions/observations alone | Small Tiny familiar gains; seed-dependent CC effects; plateau remains | Fixed-pool reuse is not a sufficient dominant explanation under the tested schedule |
| Higher post-4K learning rate | Small Tiny gains, CC regressions; full gates fail | Local trainability does not guarantee sustained held-out improvement |
| Variance-weighted query objective | Some excluded/structure gains survive incorrect pairings and can grow | Calibration changes cannot be attributed specifically to improved acquisition |
| Hidden-gate reset | Trainability improves while familiar query accuracy regresses | Opening a gate is insufficient |
| Restricted offline direction distillation | Suppressed writes and no reliable acquisition improvement | A supplied narrow direction basis did not solve credit assignment |
| Tiny_H2 recurrent history / CC_R2 extra retrieval | Matched reset/context controls reproduce the main improvements | Added memory availability is not a demonstrated mechanism benefit in that pilot |
| Full support-state optimizer fitting | Support error can approach zero while independent-query error worsens | Interpolation is not the scientific success endpoint |
| CC data×clipping factorial | Broad gates fail; Fourier subgroup succeeds, composition confirmation fails | These bounded training repairs do not restore broad original-prior learning |

Active gradients and parameter changes after 4K contradict a global vanishing-gradient explanation. Limited write directions, loss conditioning, sample-size interference, context compression and optimization remain interacting hypotheses. No unique cause or universal capacity ceiling is established.

## Phase 3 — Generalization: open

Excluded whole generating programs include order statistics, periodic remainder, signed fractional laws and localized chirps; their primitives can overlap training. A held-out program score is useful evidence but does not establish arbitrary unfamiliar relationship discovery. The target is consistent independent-query improvement, specific causal acquisition tests and transfer beyond supplied primitives.

## Phase 4 — Sustained pretraining: blocked by evidence

Scaling is a research goal conditioned on overcoming the observed plateau. The latest gates failed. This evidence does not justify portraying additional training as a proven remedy or retrospectively choosing a favorable checkpoint.

## Phase 5 — Independent validation: planned

Expand genuinely untouched dataset and environment tests, separate evidence count from recency, assess reliability and latency under deployed workloads, and enable independent replication through a deliberate asset/licensing decision. Agent adaptation and personalization have no validated results in this release. This roadmap initiates no new training or release.

Source reports and hashes: [provenance.json](../benchmarks/provenance.json). Full benchmark conditions: [results.md](../benchmarks/results.md).
