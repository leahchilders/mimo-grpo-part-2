# What changed in the music (descriptive)

Aggregates over all 928 held-out test pieces at each evaluated checkpoint (steps 0, 50, …, 300; same prompts and
sampling seeds at every step). One training run, with no run without the reward and
no KL term in the loss, so every change here is a correlation with training on this reward, not a proven effect of
it.

**Conventions**
- Unless a measure says `full_piece`, it is counted on the model's **completion** only (the music after the prompt).
  `scorer_*` and `subscore_*` are the MiMo scorer's own raw features and 0–1 subscores, on the full scored piece.
- Marks are counted on the model's own notation; spanning marks (hairpins, slurs, pedal, octave shifts) at their
  starts. Staccato includes staccatissimo; accent includes strong accent; `all` is the sum of the 11 main families
  (staccato, accent, tenuto, fermata, hairpins, dynamics, slurs, pedal, trills, arpeggio, grace notes); `all_plus`
  adds pedal changes, octave shifts, mordents and turns, tremolos, tempo changes and breath marks/caesuras.
- Rates are ratios of sums over pieces: "per 100 bars" is total marks ÷ total completion bars.
- CIs are 95% bootstrap intervals, resampling the 116 prompts within prompt kind, paired across steps; B = 2,000.
- Bar matching for repetition: `bars_pitch_rhythm` compares each bar's notes and rhythm (marks ignored);
  `bars_exact_with_marks` includes the marks; `bars_rhythm_only` ignores pitch; `bars_pitch_class_set` compares
  only which of the 12 pitch classes a bar uses. "Second-half novelty" is the share of second-half bars that never
  occur in the first half. A "loop" is a cell of up to 8 bars repeated at least 3 times in a row.
- Tokens: `longest_self_repeat_*` and `tempo_mark_*` count the model's own notation tokens.

| File | What | Source |
|---|---|---|
| `changes_step0_vs_step300.csv` | Every measure at step 0 and step 300, the difference and the relative change, with CIs (189 measures: density, expression, dynamic range, repetition and variety, register, key, endings, scorer features) | the extended "what changed" analysis (`changes2.json`) |
| `changes_by_step.csv` | The same measures at every checkpoint, long format | `changes2.json` |
| `expression_mark_totals.csv` | Total marks of each kind at each step | `changes2.json` |
| `dynamic_level_counts.csv` | How many marks of each dynamic level (pppp … ffff, plus sfz, fz and fp), step 0 and 300 | `changes2.json` |
| `repeat_share_by_density_band.csv` | Repeat share and second-half novelty within bands of notes per bar (pieces with ≥ 8 bars), to check that repetition didn't fall only because bars got denser | `changes2.json` |
| `gate_census.csv` | Why pieces scored 0, by abc2midi failure class, at every step. Classes overlap. | `changes2.json` |
| `with_vs_without_marking.csv` | Valid rate and mean reward of pieces with vs without a marking (full piece). Raw gaps mislead: heavily marked pieces also carry other risky notation. | `changes2.json` |
| `ablation.csv` | Delete one kind of marking from the scored ABC, hold the rest fixed, re-score. This measures the scorer's sensitivity to the mark, not what the model would have written instead. | `changes2.json` |
| `length_and_ending_by_step.csv` | Ended rate, length-limit rate, completion length in tokens, seconds and bars, density, distinct pitches, voices, with the change vs step 0 | the first "what changed" analysis (`changed.json`) |
| `truncation.csv` | Pieces that hit the 2,048-token limit, and how the scorer treated them | `changed.json` |
| `by_prompt_kind.csv` | Ended rate, median completion length, valid rate and median seconds per prompt kind | `changed.json` |
| `voice_counts.csv` | Pieces with 1, 2, 3 and 4 voices | `changed.json` |
| `velocity_probe.csv` | Re-scoring the listening pieces' MIDI with every velocity set to 80, and with velocities inverted. Rows for the six compared pieces (P03, P04, P13), plus the largest change over all 30 listening pieces. The scorer barely hears velocity (dynamics, hairpins). | the velocity probe (`velprobe_out.txt`) |

**Wording the article follows:** "consistent with", not "the reward caused"; staccato's fall per bar is borderline
(CI [−33%, −1%]); pedal's is not significant.
