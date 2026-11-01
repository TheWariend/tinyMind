# Figure sources

All numerical figures read public aggregate CSVs. Run `python3 reproducibility/render_figures.py` from the repository root. Points are saved measurements; curves join measured points without extrapolation. Error bars preserve audited paired 95% intervals. Seeds are separate observations, not ensemble predictions.

| Figure | Public inputs | Exact selection / transformation |
| --- | --- | --- |
| [Architecture](architecture.svg) | [Architecture description](../docs/architecture.md) and source hashes in [provenance](../benchmarks/provenance.json) | Authored explanatory diagram of native models and experimental Tiny_Global; parameter counts from reviewed architecture/report evidence |
| [Matched effects](matched-effects.svg) | [public-results.csv](../benchmarks/public-results.csv) | `plateau_repair`, `final`, Tiny_Global/Tiny_Basis_current and CC_G/CC_R, seeds 1811/1877; familiar all-K, K16–64, excluded, structure, unseen-D; preserved intervals |
| [Original pretraining](original-pretraining.svg) | [fresh-experience-curves.csv](../benchmarks/source-data/fresh-experience-curves.csv) | Tiny_B/CC_B, familiar, seeds 1811/1877, steps 1K/4K/8K; arithmetic mean over five K cells in that bank; percentages compare 4K→8K |
| [Plateau repair](plateau-repair.svg) | [plateau-curves.csv](../benchmarks/source-data/plateau-curves.csv) | Familiar final bank, original Tiny_R/CC_R and selected Tiny_Global/CC_G, steps 4K/6K/8K, each seed separately; Tiny comparison includes mathematical correction |
| [Causal evidence](causal-evidence.svg) | [public-results.csv](../benchmarks/public-results.csv) | `plateau_causal`, all K, history_off/freeze_hidden/history_wrong_labels; displayed increase is minus the saved error-reduction percentage, with interval signs/order reversed |
| [Efficiency](efficiency.svg) | [transformer-efficiency.csv](../benchmarks/source-data/transformer-efficiency.csv) | Same-study Column/Standard 1301/1337; whole-bank forward MAC /10¹², maximum cache bytes /2²⁰, adaptation + 64-query amortized milliseconds |
| [Real-world](real-world.svg) | [beijing-accuracy.csv](../benchmarks/source-data/beijing-accuracy.csv) | All K for six explicitly labeled methods, plus their K64 point estimates; all eleven methods remain in the source table. No uncertainty claim is made by bars |
| [Curriculum subgroups](curriculum-subgroups.svg) | [public-results.csv](../benchmarks/public-results.csv) | `plateau_CC_curriculum`, final CC_D/CC_R, Fourier1/composition, D4/K32–64, both seeds; unadjusted exploratory intervals |

Source identifiers and artifact/export SHA256 hashes are in [provenance.json](../benchmarks/provenance.json). Scientific conditions and caveats are in [results.md](../benchmarks/results.md). SVGs contain no raw observations, personal information, absolute filesystem paths or model implementation.
