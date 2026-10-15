"""One place for every external path. Each comes from an env var, with a default relative to the repo root.

  MIMO_SCORER_DIR  dir that contains the upstream `scorer` package
                   (default: third_party/mimo_verl/recipes/design/music)
  ABC2MIDI_BIN     abc2midi binary, version 5.04          (default: third_party/abcmidi/abc2midi)
  XML2ABC          the PATCHED xml2abc.py (version 177 + patches/xml2abc-177.patch)
                   (default: third_party/xml2abc_patched/xml2abc.py)

Importing this module also sets ABC2MIDI_BIN in the environment (the scorer reads it at import time) and puts
the upstream scorer on sys.path, so `import scorer` gives the unmodified upstream package.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(var, default):
    v = os.environ.get(var)
    return os.path.abspath(v) if v else os.path.join(ROOT, default)


MIMO_SCORER_DIR = _path("MIMO_SCORER_DIR", "third_party/mimo_verl/recipes/design/music")
ABC2MIDI_BIN = _path("ABC2MIDI_BIN", "third_party/abcmidi/abc2midi")
XML2ABC = _path("XML2ABC", "third_party/xml2abc_patched/xml2abc.py")
EXAMPLES = os.path.join(ROOT, "examples")

os.environ["ABC2MIDI_BIN"] = ABC2MIDI_BIN
if not os.path.isdir(os.path.join(MIMO_SCORER_DIR, "scorer")):
    sys.exit(f"MiMo scorer not found at {MIMO_SCORER_DIR}/scorer; run ./setup.sh or set MIMO_SCORER_DIR.")
if not os.path.isfile(XML2ABC):
    sys.exit(f"xml2abc not found at {XML2ABC}; run ./setup.sh or set XML2ABC.")
if not os.access(ABC2MIDI_BIN, os.X_OK):
    sys.exit(f"abc2midi not found at {ABC2MIDI_BIN}; run ./setup.sh or set ABC2MIDI_BIN.")
sys.path.insert(0, MIMO_SCORER_DIR)
