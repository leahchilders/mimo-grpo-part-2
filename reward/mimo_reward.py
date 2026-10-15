"""The Part 2 reward, from MusicXML: MusicXML -> xml2abc (patched v177) -> ABC -> the unmodified MiMo scorer.

During training, each Neurallegro output went tokens -> MusicXML (Neurallegro's own decoder, which is private and not
in this repo) -> this route. So the public route starts from MusicXML.

    MusicXML --xml2abc -d 16 --nbr--> ABC --normalize (drop !N! fingerings, move U: lines above K:)-->
    "```abc\\n...\\n```" --scorer.compute_score("music", ...)--> reward in [0, 1]

compute_score is the upstream function that grades a model's answer: it pulls the ABC out of the fence, runs abc2midi,
applies MiMo's gates (any abc2midi "Error", >= 10 bar-length warnings, blank lines, channel conflicts -> 0) and
otherwise returns the clamped score. The conversion and normalisation are the same as Part 1's canon route
(experiments/canon/score_one.py in the Part 1 repo).

Failure rules for MusicXML that never reaches the scorer (the same rules the training reward used):
  no pitched note at all (all rests)         -> 0.0       status "all_rest" (xml2abc writes no voices or K: here)
  xml2abc crash with "KeyError: 1"            -> 0.0       status "xml2abc_fail" (an empty right-hand staff)
  any other xml2abc crash                     -> None      status "xml2abc_fail"; training left these pieces out of
                                                           their GRPO group instead of scoring them
  timeout                                     -> 0.0       status "timeout"
In training, a decoder exception also scored 0; that step is not part of this repo.

Use:
    import sys; sys.path.insert(0, "<repo>/reward")
    from mimo_reward import score_musicxml
    r = score_musicxml("examples/P13_step300.musicxml")   # r["reward"], r["abc"], r["gates"], ...
"""
import os
import re
import subprocess as sp
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
import config  # noqa: E402  sets ABC2MIDI_BIN and puts the upstream scorer on sys.path
from scorer import compute_score  # noqa: E402
from scorer.pipeline import do, extract_abc  # noqa: E402


def normalize(abc):
    """Drop xml2abc's !N! fingering decorations and move U: lines above K: (as Part 1)."""
    abc = re.sub(r"!\d+!", "", abc)
    lines = abc.split("\n")
    u = [l for l in lines if l.startswith("U:")]
    lines = [l for l in lines if not l.startswith("U:")]
    k = next(i for i, l in enumerate(lines) if l.startswith("K:"))
    return "\n".join(lines[:k] + u + lines[k:])


def musicxml_to_abc(path, timeout=60):
    """-> (abc or None, xml2abc stderr). abc is normalised and stripped: the exact text the scorer scores."""
    p = sp.run([sys.executable, config.XML2ABC, "-d", "16", "--nbr", path], capture_output=True, timeout=timeout)
    raw = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    if "K:" not in raw:
        return None, err
    return normalize(raw).strip(), err


def gates(abc):
    """Which of MiMo's gates fire for this ABC (diagnostic only; the reward comes from compute_score)."""
    r = do(dict(key="k", id=0, rep=0, abc=abc, tag=None, lang=None, abc_len=len(abc), nvoice=0, latency=None))
    g = []
    if r.get("skip"): g.append("skip:" + str(r["skip"]))
    if r.get("err", 0) > 0: g.append(f"abc2midi_Error x{r['err']}")
    if r.get("bar", 0) >= 10: g.append(f"bar_warnings x{r['bar']}")
    if r.get("blank"): g.append("blank_line")
    if r.get("ch_conflict", 0) > 0: g.append(f"ch_conflict x{r['ch_conflict']}")
    if "total" not in r and not r.get("skip"): g.append("no_total")
    return ";".join(g), r.get("total")


def score_musicxml(path, timeout=60):
    xml = open(path, encoding="utf-8").read()
    if "<pitch>" not in xml:
        return dict(path=path, status="all_rest", reward=0.0, abc=None)
    try:
        abc, err = musicxml_to_abc(path, timeout)
    except sp.TimeoutExpired:
        return dict(path=path, status="timeout", reward=0.0, abc=None)
    if abc is None:
        last = (err.strip().splitlines() or ["?"])[-1][-150:]
        return dict(path=path, status="xml2abc_fail", reward=0.0 if "KeyError: 1" in err else None,
                    abc=None, xml2abc_err=last)
    reward = compute_score("music", "```abc\n" + abc + "\n```")
    assert extract_abc("```abc\n" + abc + "\n```") == abc
    g, total = gates(abc)
    return dict(path=path, status="ok", reward=round(reward, 4), quality_ungated=total, gates=g, abc=abc)


if __name__ == "__main__":
    import json
    for f in sys.argv[1:]:
        r = score_musicxml(f)
        r.pop("abc", None)
        print(json.dumps(r))
