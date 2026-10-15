# Training My Model on a Bad Scorer Made It (Slightly) Better

Code, data and media for the article: https://leahchilders-portfolio.vercel.app/music-ml/mimo-grpo-part-2

Part 2 of a series on verifiable rewards for music notation. In Part 1 I took apart the music reward Xiaomi released
with MiMo-V2.6 (code and the scorer audit: https://github.com/leahchilders/mimo-reward-hacking-part-1). In Part 1 I said the scorer was a problem because it was on its way to actually be used in real training frameworks, so I decided to use it to post-train my own music composition transformer and see what happens.

- **The model.** Neurallegro, my own small (25.5M-parameter) transformer. It writes piano music in its own token format,
  not MusicXML, ABC or MIDI, so it can't be fed to the scorer directly. It isn't open source (yet), so this repo has no weights, no generation code and only eight of its pieces.
- **The training.** 300 steps of GRPO (without std normalization, Dr. GRPO-style) with MiMo-V2.6's released scorer, unmodified, as the reward: 8 prompts ×
  8 samples per step, learning rate 1e-5, no KL penalty. About 70 minutes on a laptop GPU.
- **The score.** On 928 held-out test pieces (116 prompts × 8 samples), the mean score rose from **0.606 to 0.772**.
  - The share of pieces that got a score at all went from 82% to 95%, and the mean among those went from 0.736 to
    0.810.
  - The single best piece didn't improve (0.969 at step 0, 0.957 at step 300), but pieces scoring 0.9 or above went
    from 28 to 98.
  - With header-only prompts, where every note is the model's, it went from 0.639 to 0.790.
- **No known hack grew.** None of Part 1's tricks became more common, and re-scoring with each checked trick undone
  leaves the whole gain (F = 1.003).
- **The listening.** In a blind A/B test of 15 pairs, I preferred the trained piece in **11 of 15**. A sign test gives p = 0.12: a direction, not a
  significant result.
- **What changed.** About 42% more notes per bar in about the same number of bars, less exact repetition, and about
  a third fewer expressive markings per bar.

This is one training run, one seed and one listener (me, the author). It's not a rigorous result.

## What's here

- `media/`: the audio, score PDFs, Sibelius files and figure used in the article: its three comparisons (the "O Come All Ye
  Faithful" continuation (P03), the header-only piece (P13) and the march continuation (P04)) and its two best pieces
  (the highest-scoring test piece before and after training).
- `examples/`: those eight pieces as MusicXML, the ABC the scorer scored and abc2midi's MIDI, with their stored
  scores (`scores.json`). See `examples/README.md`, including the note on the march pieces' article audio (dynamics
  fixed for the article; the scorer, and for P04 the blind listening, used the unfixed version).
- `reward/`: the reward from MusicXML: `mimo_reward.py` (MusicXML → patched xml2abc → ABC → the upstream scorer's
  `compute_score`) and `score_examples.py`, which re-scores the eight examples.
- `patches/xml2abc-177.patch`: the three crash fixes to xml2abc v177 that the reward used, with what each changes and
  why.
- `results/`: the aggregate numbers behind the article, as CSV, each folder with a README:
  - `headline/`: step 0 vs step 300, by prompt kind, per-prompt change, the reference lines and the gain
    decomposition;
  - `controls/`: the hack controls (tags) at every checkpoint;
  - `curve/`: per-step training data, the held-out evals at steps 0–300, and `make_figure1.py` for Figure 1;
  - `changes/`: what changed in the music (density, expression, repetition, endings, rejections).
- `listening/`: the blind listening protocol and the 15 choices with their step labels.
- `common/config.py`: all external paths, from env vars.
- `setup.sh`: fetches the upstream scorer, abc2midi and xml2abc into `third_party/` (gitignored) and applies the
  patch.

## Reproduce

Run `./setup.sh` (it needs git, curl, unzip, patch, a C compiler and make), then
`python reward/score_examples.py`. It converts each example's MusicXML, scores it, and checks that both the ABC and
the score match what was stored during the run. All eight match (step 0 / step 300: P03 0.747 / 0.929, P13 0.734 / 0.876, P04 0.866 / 0.885; best pieces 0.969 at step 0, 0.957 at step 300). Or
point `MIMO_SCORER_DIR`, `ABC2MIDI_BIN` and `XML2ABC` at existing copies (see `common/config.py`). The scorer and
the reward are stdlib-only Python (tested with 3.12). `python results/curve/make_figure1.py` redraws Figure 1 from
the CSVs (needs `pip install -r requirements.txt`).

What isn't reproducible from this repo: the training, the generation, and the step from the model's tokens to
MusicXML, since the model and its decoder are private. So the public route starts from MusicXML. The CSVs in
`results/` are exported from the run's analyses, which read per-piece data that isn't released.

## Licenses

Code: MIT (see `LICENSE`). Media in `media/` (audio renders, PDFs, Sibelius files, figure): CC BY 4.0 (see
`media/LICENSE`). The audio was rendered with the Salamander Grand Piano by Alexander Holm (CC BY 3.0), in FreePats'
SF2 conversion. `patches/xml2abc-177.patch` modifies xml2abc, so it is under xml2abc's LGPL.

Data in `examples/`, `results/` and `listening/` (CSV tables, MusicXML, ABC, MIDI, the listening protocol): CC BY 4.0
(see the `LICENSE` file in each folder). The scripts in `results/curve/` and `reward/` are code, under MIT.

In the examples, P03's first two bars (the pickup and the first full bar) are "Adeste Fideles" ("O Come All
Ye Faithful"), arr. Samuel Webbe (public domain), and P04's first four bars are an opening written for testing this
project. The two best pieces continue the same two prompts (the step-300 best from P03's opening, the step-0 best from
P04's seed). Everything else is model output.
