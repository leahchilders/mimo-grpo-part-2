# Examples

The eight pieces shown in the article: three test prompts, each with one piece from before training (step 0) and one
from after (step 300), plus the two best pieces (the highest-scoring of the 928 test pieces at step 0 and at step 300).
These are the only generations in this repo.

| Pair | Prompt | Step 0 score | Step 300 score |
|---|---|---|---|
| P03 (Comparison 1, the "O Come All Ye Faithful" continuation) | Opening: the first 2 bars (the pickup and the first full bar) of "Adeste Fideles" ("O Come All Ye Faithful"), arr. Samuel Webbe (public domain). The model starts at bar 3 of the MusicXML. | 0.747 | 0.929 |
| P13 (Comparison 2, the header-only piece) | Header only: 4 flats, 3/4, tempo 96, treble and bass clefs, no notes. Every note is the model's. | 0.734 | 0.876 |
| P04 (Comparison 3, the march continuation) | Seed: a 4-bar march opening written for testing this project. The model starts at bar 5 (at step 300 it also added one note to the last chord of bar 4). | 0.866 | 0.885 |

| Best piece | Prompt | Score |
|---|---|---|
| `best_step0` (the base model's best) | The same march seed as P04 (a different sample). The model starts at bar 5 (like P04 at step 300, it also added one note to the last chord of bar 4). | 0.969 |
| `best_step300` (the trained model's best) | The same "Adeste Fideles" opening as P03 (a different sample). The model starts at bar 3. | 0.957 |

The best pieces were not part of the blind listening (they come from the other sampling seed of the evaluation).

Scores are the rewards stored during the run (`scores.json`). `python reward/score_examples.py` recomputes them from
the MusicXML.

## Files, per piece (`<pair>_step<0|300>`)

- `.musicxml`: the model's output as MusicXML, prompt included. This is where the public route starts (the step
  before it, from the model's tokens to MusicXML, uses the model's private decoder).
- `_marked.musicxml` (P03, P04 only; not the best pieces): the same file with one text direction, "model begins", at the first bar the
  model wrote. Nothing else differs. These were imported into Sibelius for the engravings in `media/`.
- `.abc`: the ABC the scorer scored, exactly as stored during the run (xml2abc output after the normalisation in
  `reward/mimo_reward.py`).
- `_abc2midi.mid`: abc2midi 5.04's MIDI of that ABC. This is what the scorer measured, what the blind listening
  heard (through a General MIDI piano) and what the article's audio was rendered from (except the march pieces'; see below).

## The march pieces' article audio (dynamics fixed)

`P04_step0_dynfix.abc`, `P04_step300_dynfix.abc` and `best_step0_dynfix.abc` (the best piece is also a march
continuation) were made for the article's audio only. **The scorer never saw them; it scored `P04_step*.abc` and
`best_step0.abc`.** The blind listening used the unfixed P04 versions too.

Two changes, both to dynamics:
1. Every dynamic and hairpin is applied to every voice. xml2abc puts a dynamic that sits between the staves in one
   voice only, and abc2midi applies dynamics per voice, so in the scored version the left hand never gets any.
2. `p` is replaced by `mp`, because `p` was far too quiet in this render.

Each rendered file was then set, as a whole, to −24 LUFS, the level of the other renders (volume only). The
notes are unchanged (the best piece's repeat signs too). If you score the fixed ABC anyway, P04 gets 0.864 (step 0)
and 0.882 (step 300), against 0.866 and 0.885 for what was actually scored; the best piece gets 0.969 either way. The difference comes from the one velocity-weighted feature in the scorer (`roughness_p90`).
