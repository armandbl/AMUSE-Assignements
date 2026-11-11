#!/usr/bin/env bash
#
# setup_nbstripout.sh
# -------------------
# One-command setup: install nbstripout into the *active* Python environment
# (your AMUSE env) and configure git so notebook outputs and run counts
# (execution_count) are never committed.
#
# HOW TO USE
# ----------
#   1. Activate your AMUSE environment:
#        conda activate Amuse-env        # <- your env name
#   2. cd to the root of a git repository.
#   3. Run:
#        bash setup_nbstripout.sh
#   4. Review and commit:
#        git status
#        git diff --cached --stat
#        git commit -m "Strip notebook outputs and run counts"
#
# WHAT IT DOES
# ------------
#   1. pip-installs nbstripout into the active env.
#   2. `nbstripout --install` configures the git filter:
#        filter.nbstripout.clean    -> "<python> -m nbstripout"   (strips on commit)
#        filter.nbstripout.smudge   -> cat                        (leaves your file as-is on checkout)
#        filter.nbstripout.required -> true                       (error out rather than silently keep outputs)
#        diff.ipynb.textconv        -> "<python> -m nbstripout -t" (nice text diffs)
#      and appends "*.ipynb filter=nbstripout" / "*.zpln filter=nbstripout"
#      to .gitattributes if missing.
#   3. `git add --renormalize .` re-stages every tracked notebook through the
#      clean filter, so outputs + execution counts that were already committed
#      are stripped from the index in one go.
set -euo pipefail

# --- 1. Install nbstripout into the active environment -----------------------
echo ">> Installing nbstripout..."
python -m pip install --upgrade nbstripout

# --- 2. Configure the git filter + .gitattributes ----------------------------
echo ">> Configuring the git filter..."
python -m nbstripout --install

# --- 3. Re-normalise already-tracked notebooks -------------------------------
echo ">> Re-staging tracked notebooks through the clean filter..."
git add --renormalize .

echo
echo "Done. Review what changed, then commit:"
echo "  git status"
echo "  git diff --cached --stat"
echo "  git commit -m 'Strip notebook outputs and run counts'"
