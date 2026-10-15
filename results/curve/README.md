# Training curve and Figure 1

| File | What | Source |
|---|---|---|
| `train_steps.csv` | One row per GRPO step (1–300): mean training reward over that step's 64 rollouts (8 training prompts × 8 samples; rejected = 0), its trailing 20-step mean, valid rate, mean among valid, header and opening means, mean completion length, share of completions cut at the length limit, share of groups with zero reward spread, logged KL to the starting model (k3 estimator, per token; logged only, not in the loss) and entropy | the run's per-step log, via the curve analysis (`curve.csv`) |
| `eval_points.csv` | The held-out test eval at steps 0, 50, 100, 150, 200, 250 and 300 (928 pieces each, same prompts and seeds): mean over all with its 95% bootstrap CI, valid rate with CI, mean among valid, ended rate, and the same per prompt kind. The `role` column marks steps 0 and 300 (`step0_vs_step300`, the main comparison) and the snapshots in between (`snapshot`). | the curve analysis (`eval_points.csv`), with internal path and hash columns dropped |
| `among_valid_ci.csv` | Mean among valid at each eval, with a bootstrap CI | the figure analysis (`among_valid_ci.csv`) |
| `make_figure1.py` | Draws Figure 1 (no title; legend "All test pieces (rejected pieces score 0)" and "Test pieces that got a score", each with its 95% bootstrap band; canonical composers' pieces that got a score as a dotted grey line; random notes in 2 and 3 voices as dashed lines) from the two CSVs above and `results/headline/reference_lines.csv`. Its PNG output is byte-identical to `media/img/held-out-score-{light,dark}.png`. | the figure script (variant e), with paths made relative |

Training prompts (header-only prompts and openings from a validation split) are different from the test prompts in
`eval_points.csv`, so the train and test curves are not strictly comparable.
