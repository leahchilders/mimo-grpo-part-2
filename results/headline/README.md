# Headline numbers

Step 0 (before training) vs step 300 (after), unless a row says otherwise. Each checkpoint was evaluated on the same 116 held-out test prompts × 8 samples = 928 pieces,
with the same sampling seeds. No piece was excluded at either checkpoint.

- **"Mean over all" (`mean_all`)** counts a piece the scorer rejects (abc2midi error, ≥ 10 bar-length warnings and
  so on) as 0. **"Valid"** means the piece got a score above 0. **"Mean among valid"** averages only those.
- **CIs** for `mean_all` and `valid_rate` are a two-stage bootstrap (prompts, then samples within
  a prompt), stratified by prompt kind, 10,000 resamples. The CI for `mean_among_valid` is a bootstrap over prompts
  made for the figure.

| File | What | Source |
|---|---|---|
| `headline.csv` | Step 0 vs 300: mean over all, valid rate, mean among valid, max, top-10 mean, rate of pieces that ended on their own (vs hitting the 2,048-token limit) | `results.json`, `headline`; the among-valid CI from the figure analysis (`among_valid_ci.csv`) |
| `by_prompt_kind.csv` | The same, split by prompt kind. `test_header` = header only (key signature, time signature, clefs, usually a tempo, no notes); `test_opening` = the first 2 bars of a held-out PDMX piece; `seed` = short openings written for testing; `tune` = short arrangements of well-known tunes. Descriptive. | `results.json`, `headline` |
| `per_prompt_change.csv` | Each prompt's mean at step 300 minus its own mean at step 0. Descriptive. | `results.json`, `per_prompt_delta_descriptive` |
| `reference_lines.csv` | The same scorer on Part 1's canonical pieces and random notes | `results.json`, `reference_lines` (numbers from Part 1); Part 1's best hack from Part 1's README |
| `high_scores.csv` | Step 0 vs 300: how many of the 928 pieces scored at least 0.8, 0.9 and 0.93, and the single best score. Descriptive. | the stored rewards in the run's eval batches (computed 10-14) |
| `gain_decomposition.csv` | How much of the +0.166 came from more pieces passing (validity) and how much from higher scores among the passing pieces (quality). Descriptive. | the "what changed" analysis (`changes2.json`, `hypothesis.gain_decomposition`) |

**One run.** One training seed, one listener.
