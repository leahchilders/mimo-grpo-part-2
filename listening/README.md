# Blind listening

One listener (the author) compared 15 pairs, blind, before seeing any scores. Each pair is one piece from before
training (step 0) and one from after (step 300), continuing the same test prompt.

`choices.csv` has one row per pair:
- `prompt_kind`: `test_header` (no notes in the prompt), `test_opening` (the first 2 bars of a held-out PDMX piece)
  or `seed` (a short opening written for testing);
- which checkpoint was heard as "A" and which as "B";
- the letter chosen and the checkpoint that means (`preferred_step`);
- `step300_truncated`: "yes" when the step-300 piece hit the 2,048-token limit and stops mid-phrase;
- `shown_in_post`: P03, P04 and P13 are the pairs in the article (audio and files in `media/` and `examples/`).

Source: the listening key (A/B order per pair) and the un-keyed result (`KEY.json`, `unkey_results.json`).

## Protocol

- **Draw.** 15 prompts drawn at random (fixed seed) from the 115 test prompts where both checkpoints produced a piece
  that got a score. For each checkpoint, one of that prompt's scored pieces was picked by a fixed seeded rule.
- **Order.** A/B order drawn once per pair with an unseeded system RNG and stored only in the key. Step 300 was "A"
  in 8 of the 15 pairs.
- **Audio.** The scored ABC → abc2midi 5.04 → program changes stripped → FluidSynth 2.3.4 with the FluidR3_GM
  General MIDI piano, gain 0.5, 44.1 kHz. 0.58 hours of audio in all; the longest file was 6.3 minutes.
- **Question.** "Which of the two is the better piece of music?" Forced choice: A or B, no ties.
- **Listening rule:** "listen as long as you wish; you may skip or stop; judge on what you
  heard."
- **Blinding.** The answers were locked in before the key was opened.

## Result

- Step 300 preferred in **11 of 15** pairs (step 0 in 4).
- Exact two-sided sign test for 11 of 15: p = 2 × (C(15,11) + C(15,12) + … + C(15,15)) / 2^15 = 2 × 1941 / 32768
  = **0.1185**. A direction, not significance.
- By prompt kind: header only 5 of 5 for step 300; openings 5 of 8; seeds 1 of 2.

## Disclosures

- One listener, who is the author and built the model, and knows its sound.
- The listener's stated prior was "bad scorer".
- The two seed prompts (P04, P06) were written for this project, so the listener may recognise them.
- The blinding is weaker than "same prompt, same render". The step-300 piece was longer in
  tokens in 11 of 15 pairs and in seconds in 9 of 15, and had more hairpin marks in 4 pairs (fewer in none).
