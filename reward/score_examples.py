"""Re-score the example pieces from their MusicXML and compare with the rewards stored during the run.

    python reward/score_examples.py

For each piece in examples/scores.json it runs reward/mimo_reward.py on examples/<piece>.musicxml and checks:
  - the recomputed reward equals the stored reward (the run stored it at 3 decimals; the scorer's total is
    reported to 0.1 points, so 3 decimals is its full precision);
  - the ABC it produced is byte-identical to examples/<piece>.abc (the text that was scored during the run).
Exit status 1 if anything differs.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mimo_reward import score_musicxml  # noqa: E402
import config  # noqa: E402  (already on sys.path via mimo_reward)

rows = json.load(open(os.path.join(config.EXAMPLES, "scores.json")))
bad = 0
print(f"{'piece':<13} {'stored':>7} {'recomputed':>10}  {'ABC identical':<13} gates")
for row in rows:
    r = score_musicxml(os.path.join(config.EXAMPLES, row["musicxml"]))
    want_abc = open(os.path.join(config.EXAMPLES, row["abc"]), encoding="utf-8").read().strip()
    same_abc = r["abc"] == want_abc
    same_reward = r["reward"] is not None and round(r["reward"], 3) == row["stored_reward"]
    bad += not (same_abc and same_reward)
    print(f"{row['piece']:<13} {row['stored_reward']:>7.3f} {r['reward']:>10.4f}  {str(same_abc):<13} {r.get('gates') or '-'}")
print(f"all {len(rows)} match" if not bad else f"{bad} piece(s) differ")
sys.exit(1 if bad else 0)
