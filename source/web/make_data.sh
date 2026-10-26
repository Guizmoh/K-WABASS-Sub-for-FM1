#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# The DATA page (backup / restore, WAV export, samples): web/data.html with web/kwlink.js put in -> ../data.html
set -e
cd "$(dirname "$0")/.."
python3 - <<'PY'
from pathlib import Path
page = Path("web/data.html").read_text().replace("__KWLINK_JS__", Path("web/kwlink.js").read_text())
Path("../data.html").write_text(page)
print("data.html", len(page), "B")
PY
