#      TinyType is a minimal typing test software that sits in the corner of your screen while you work!
#      Copyright (C) 2026  Jon Evans
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

from project_info import Info

# ---------------------------------------------------------------
# Paths
# ---------------------------------------------------------------
ROOT        = Path(__file__).parent.resolve()
VENV        = ROOT / "venv" / "Scripts"
PYINSTALLER = VENV / "pyinstaller.exe"
SPEC        = ROOT / "build.spec"
BUILDS_DIR  = ROOT / "builds"
LOG_FILE    = ROOT / "build_log.txt"

VERSION     = Info.VERSION

# ---------------------------------------------------------------
# Log header
# ---------------------------------------------------------------
timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
header = (
    f"\n\n\nNEW BUILD STARTED\n=========\n"
    f"{datetime.now().strftime('%d %B, %Y %H:%M,%S')}\n"
    f"Version: {VERSION}\n\n\n"
)
with open(LOG_FILE, "a") as log:
    log.write(header)

# ---------------------------------------------------------------
# 0. Generate favicon.ico from favicon.png (PyInstaller needs .ico)
# ---------------------------------------------------------------
print("[build] Generating favicon.ico from favicon.png ...")
icon_result = subprocess.run(
    [str(VENV / "python.exe"), str(ROOT / "make_icon.py")],
    capture_output=True,
    text=True,
)
print(icon_result.stdout.strip())
if icon_result.returncode != 0:
    print("[build] WARNING: could not generate favicon.ico — building without exe icon")
    print(icon_result.stderr.strip())

# ---------------------------------------------------------------
# 1. PyInstaller
# ---------------------------------------------------------------
print(f"[build] Running PyInstaller for {Info.PROJECT_TITLE} v{VERSION} ...")
with open(LOG_FILE, "a") as log:
    result = subprocess.run(
        [str(PYINSTALLER), str(SPEC)],
        stderr=log,
        stdout=log,
        shell=True,
    )

if result.returncode != 0:
    print("[build] PyInstaller FAILED — check build_log.txt")
    sys.exit(result.returncode)

print("[build] PyInstaller succeeded.")

# ---------------------------------------------------------------
# 2. Find the newest build output directory
# ---------------------------------------------------------------
build_dirs = sorted(
    (d for d in BUILDS_DIR.iterdir() if d.is_dir() and d.name.startswith(Info.PROJECT_TITLE)),
    key=lambda d: d.stat().st_mtime,
    reverse=True,
)
if not build_dirs:
    print("[build] Could not find PyInstaller output under builds/. Skipping installer.")
    sys.exit(0)

built_app_dir = build_dirs[0] / Info.PROJECT_TITLE
if not built_app_dir.exists():
    print(f"[build] Expected app folder not found: {built_app_dir}")
    sys.exit(0)

print(f"[build] App output: {built_app_dir}")

# ---------------------------------------------------------------
# 3. NSIS installer
# ---------------------------------------------------------------
# Try common NSIS install locations
nsis_candidates = [
    Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "NSIS" / "makensis.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "NSIS" / "makensis.exe",
    Path(r"C:\Program Files\NSIS\makensis.exe"),
    Path(r"C:\Program Files (x86)\NSIS\makensis.exe"),
]
makensis = next((p for p in nsis_candidates if p.exists()), None)

if makensis is None:
    print("[build] makensis.exe not found — skipping installer creation.")
    print("[build]   Download NSIS from https://nsis.sourceforge.io and re-run build.py")
else:
    installer_out = BUILDS_DIR / f"{Info.PROJECT_TITLE}-Setup-{VERSION}.exe"
    print(f"[build] Running NSIS to create {installer_out.name} ...")

    nsis_cmd = [
        str(makensis),
        f"/DAPP_VERSION={VERSION}",
        f"/DBUILD_DIR={built_app_dir}",
        str(ROOT / "installer.nsi"),
    ]
    with open(LOG_FILE, "a") as log:
        nsis_result = subprocess.run(nsis_cmd, stderr=log, stdout=log)

    if nsis_result.returncode != 0:
        print("[build] NSIS FAILED — check build_log.txt")
    else:
        print(f"[build] Installer created: {installer_out}")

print("[build] Done.")
