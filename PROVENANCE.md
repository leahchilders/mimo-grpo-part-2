# Provenance

## Tools

| Tool | Source | Version | License |
|---|---|---|---|
| MiMo-V2.6 music scorer | https://github.com/XiaomiMiMo/verl, branch `mimo-oss`, `recipes/design/music/scorer` | commit `a2ad9f6` | Apache-2.0 |
| abc2midi | https://github.com/sshlien/abcmidi, built from source (`./configure && make abc2midi`) | commit `11f66bb` (5.04) | GPL |
| xml2abc.py (Wim Vree) | https://wim.vree.org/svgParse/xml2abc.html (`xml2abc.py-177.zip`, sha256 `158ae6ac87c34b7f170a7a57712206fac756e0434806e38a280f6fd968c8816d`) | 177, plus `patches/xml2abc-177.patch` (patched file sha256 `0772d26f0714749ebc1964339d88282fa5d36f158ac0bd60a7b1bb245bf6b7e3`) | LGPL |
| FluidSynth | system package | 2.3.4 | LGPL |
| Salamander Grand Piano, SF2 by FreePats | https://freepats.zenvoid.org/Piano/SalamanderGrandPiano/SalamanderGrandPiano-SF2-V3+20200602.tar.xz | V3+20200602 | CC BY 3.0 (Alexander Holm) |
| FluidR3_GM (listening render only) | Ubuntu package `fluid-soundfont-gm` 3.1 | 3.1 | MIT |

The scorer and abc2midi are the same pins as Part 1. The xml2abc patch is the only change to any tool, and it only
touches code paths that used to crash (see the top of the patch file). The patched file used in the run differs from
the one `setup.sh` builds only in the wording of the three `# PATCH` comments.

## The route during training

Neurallegro tokens → MusicXML (Neurallegro's decoder; private, not in this repo) → `reward/mimo_reward.py`'s route
(patched xml2abc → normalised ABC → `compute_score`). The training reward also had a 60-second deadline per piece
(a timeout scored 0), ran six pieces in parallel, and scored a piece the decoder could not decode as 0.

## Prompts

- **Header only:** key signature, time signature, clefs and usually a tempo; no notes. They were held out of the
  training prompt pool.
- **Openings:** the first 2 bars of pieces in the test split of PDMX ("PDMX: A Large-Scale Public Domain MusicXML
  Dataset for Symbolic Music Processing", arXiv:2409.10831). PDMX's license labels are the uploader's declaration and
  describe the uploaded score file, not the copyright of the composition; some of these openings are modern songs.
  None are redistributed here except P03's two bars ("Adeste Fideles", i.e. "O Come All Ye Faithful", arr. Samuel
  Webbe, public domain).
- **Seeds:** 14 short openings (2–4 bars) written for testing this project, in different styles.
- **Tunes:** 6 short arrangements of public-domain melodies, written for testing this project.

## Audio (media/audio/)

The MIDI in `examples/*_abc2midi.mid` rendered with FluidSynth 2.3.4 and the Salamander Grand Piano V3 SF2
(gain 0.5, reverb and chorus on, polyphony 256, 44.1 kHz), then encoded to MP3 with ffmpeg 6.1.1 (libmp3lame, VBR
quality 2). The march pieces (P04's two files and `best-step0.mp3`) were rendered from `examples/*_dynfix.abc` instead (see
`examples/README.md`) with each whole file set to −24 LUFS, the level of the other renders (−23.5 to −24.4 LUFS).

## Scores (media/scores/, media/sibelius/)

Engraved by me in Sibelius 21.2.0 from `examples/*_marked.musicxml` (P03, P04) and `examples/*.musicxml`
(P13 and the two best pieces). I just changed some of the colors to indicate the prompt, nad added the prompt annotations.
