#!/usr/bin/env bash
# Fetch the third-party tools into third_party/ (gitignored). Needs git, curl, unzip, sha256sum, patch,
# a C compiler and make. Safe to re-run: each step is skipped if its output already exists.
# These are the same pins as Part 1 (github.com/leahchilders/mimo-reward-hacking-part-1), plus the xml2abc patch.
set -euo pipefail
cd "$(dirname "$0")"
REPO=$(pwd)
mkdir -p third_party
cd third_party

# 1. MiMo-V2.6 music scorer (Apache-2.0): XiaomiMiMo/verl, branch mimo-oss, commit a2ad9f6.
#    Only recipes/design/music is checked out; the scorer package is recipes/design/music/scorer. Used unmodified.
VERL_SHA=a2ad9f6160b03ff2d47e59832bfb6b289f37c917
if [ ! -d mimo_verl/recipes/design/music/scorer ]; then
  rm -rf mimo_verl
  git init -q mimo_verl
  git -C mimo_verl remote add origin https://github.com/XiaomiMiMo/verl
  git -C mimo_verl fetch -q --depth 1 --filter=blob:none origin "$VERL_SHA"
  git -C mimo_verl sparse-checkout set recipes/design/music
  git -C mimo_verl -c advice.detachedHead=false checkout -q FETCH_HEAD
fi

# 2. abc2midi (GPL), built from source: sshlien/abcmidi at commit 11f66bb (version 5.04).
ABCMIDI_SHA=11f66bb2cea9fa4537fd94c97d232f5fb4e2f8a6
if [ ! -x abcmidi/abc2midi ]; then
  rm -rf abcmidi
  git init -q abcmidi
  git -C abcmidi remote add origin https://github.com/sshlien/abcmidi
  git -C abcmidi fetch -q --depth 1 origin "$ABCMIDI_SHA"
  git -C abcmidi -c advice.detachedHead=false checkout -q FETCH_HEAD
  (cd abcmidi && ./configure && make abc2midi)
fi

# 3. xml2abc.py version 177 (Wim Vree, LGPL), from https://wim.vree.org/svgParse/xml2abc.html,
#    then patches/xml2abc-177.patch (three crash fixes; see the top of that file).
#    xml2abc/ holds the upstream file, xml2abc_patched/ the patched one the reward uses.
XML2ABC_ZIP=xml2abc.py-177.zip
XML2ABC_SHA256=158ae6ac87c34b7f170a7a57712206fac756e0434806e38a280f6fd968c8816d
PATCHED_SHA256=0772d26f0714749ebc1964339d88282fa5d36f158ac0bd60a7b1bb245bf6b7e3
if [ ! -f xml2abc/xml2abc.py ]; then
  curl -fsSL -o "$XML2ABC_ZIP" "https://wim.vree.org/svgParse/$XML2ABC_ZIP"
  echo "$XML2ABC_SHA256  $XML2ABC_ZIP" | sha256sum -c -
  mkdir -p xml2abc
  unzip -q -j -o "$XML2ABC_ZIP" -d xml2abc
fi
if [ ! -f xml2abc_patched/xml2abc.py ]; then
  mkdir -p xml2abc_patched
  cp xml2abc/xml2abc.py xml2abc_patched/xml2abc.py
  (cd xml2abc_patched && patch -s -p1 < "$REPO/patches/xml2abc-177.patch")
  echo "$PATCHED_SHA256  xml2abc_patched/xml2abc.py" | sha256sum -c -
fi

echo "third_party/ ready."
