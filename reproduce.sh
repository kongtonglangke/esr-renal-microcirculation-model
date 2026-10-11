#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Reproduce every numerical result and every manuscript figure.
#
#   ./reproduce.sh
#
# The pipeline is deterministic: re-running it rewrites results/ and figures/
# and reproduces the published values bit-for-bit, except for the run
# timestamps recorded in results/v2_package_versions.json and the
# results/*_run_log.txt files.
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")"

PY="${PYTHON:-python}"

echo "Using interpreter: $("$PY" -c 'import sys; print(sys.executable)')"
"$PY" - <<'PYEOF'
import sys
if sys.version_info < (3, 9):
    sys.exit("Python 3.9+ is required (found %s)" % sys.version.split()[0])
PYEOF

STAGES=(
  "code/esr_model_v2.py|Layers 2-3: viscosity, vessel states, cell-free layer, WSS variability"
  "code/esr_model_v3.py|Layer 1: ESR -> aggregate-size mapping from measured anchors"
  "code/esr_model_v4_flowcurve.py|Layer 4: pressure-flow curve and fold/stasis detection"
  "code/esr_model_v5_calibration.py|Layer 4: inverse calibration of the viscosity kernel"
  "code/make_ms_figures.py|Figures 1-6 (Figure 7 comes from the v4 stage)"
)

for entry in "${STAGES[@]}"; do
  script="${entry%%|*}"
  label="${entry#*|}"
  echo
  echo "=== ${script}  --  ${label}"
  "$PY" "$script"
done

# The stages also emit diagnostic intermediates (v2_fig*, ms_fig*).  Keep only
# the seven numbered manuscript figures, so that figure numbers in the paper,
# in figures/ and in the manuscript captions stay in one-to-one correspondence.
# Text output is normalised to LF so that a re-run leaves a clean `git status`
# (only the run timestamp changes).
echo
echo "=== normalising figures/ and line endings ==="
"$PY" - <<'PYEOF'
from pathlib import Path
import shutil

fig = Path("figures")
# Figure 7 is produced by the v4 stage under an internal name
for src, dst in {"ms_fig7_stasis.png": "Figure7_stasis.png",
                 "ms_fig7_stasis.tif": "Figure7_stasis.tif"}.items():
    if (fig / src).exists():
        shutil.copyfile(fig / src, fig / dst)
        (fig / src).unlink()

for p in sorted(fig.iterdir()):
    if p.is_file() and not p.name.startswith("Figure"):
        p.unlink()

print("kept:", ", ".join(sorted(p.name for p in fig.glob("Figure*.png"))))

TEXT = {".md", ".txt", ".csv", ".json"}
n = 0
for p in sorted(list(Path("results").iterdir()) + list(Path("supplementary").iterdir())):
    if p.is_file() and p.suffix.lower() in TEXT:
        b = p.read_bytes()
        if b"\r\n" in b:
            p.write_bytes(b.replace(b"\r\n", b"\n"))
            n += 1
print("line endings normalised to LF in %d files" % n)
PYEOF

echo
echo "Done. Numerical results in results/, manuscript figures in figures/."
