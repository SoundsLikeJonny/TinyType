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

from typing import Optional, Callable
import threading
import urllib.request
import json
import os
import subprocess
import tempfile

from PySide6.QtCore import QObject, Signal
# TODO: remove. USed for version testing

class Updater(QObject):
    """Checks GitHub Releases for a newer version and can download+launch the installer."""

    update_available: Signal = Signal(str, str)  # (latest_version, download_url)
    download_progress: Signal = Signal(int)       # percent 0-100
    download_finished: Signal = Signal(str)       # path to downloaded installer

    GITHUB_API = "https://api.github.com/repos/{repo}/releases/latest"

    def __init__(self, repo: str, current_version: str, parent=None) -> None:
        super().__init__(parent)
        self.repo = repo
        self.current_version = current_version
        self._installer_path: Optional[str] = None

    # ------------------------------------------------------------------
    # Version check (background thread, emits update_available if newer)
    # ------------------------------------------------------------------

    def check_async(self) -> None:
        t = threading.Thread(target=self._check, daemon=True, name="updater-check")
        t.start()

    def _check(self) -> None:
        try:
            # Use /releases endpoint so we see pre-releases too, then pick the
            # best candidate depending on whether the running version is a pre-release.
            url = f"https://api.github.com/repos/{self.repo}/releases"
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "TinyType-Updater")
            req.add_header("Accept", "application/vnd.github+json")
            with urllib.request.urlopen(req, timeout=10) as resp:
                releases = json.loads(resp.read().decode())

            if not releases:
                return

            current_is_pre = self._is_prerelease(self.current_version)

            best = None
            for rel in releases:
                tag: str = rel.get("tag_name", "").lstrip("v")
                if not tag:
                    continue
                is_pre: bool = rel.get("prerelease", False) or self._is_prerelease(tag)
                # Stable users only see stable releases.
                # Beta users see both stable and pre-releases.
                if is_pre and not current_is_pre:
                    continue
                if self._is_newer(tag, self.current_version):
                    best = (tag, rel)
                    break  # releases are newest-first

            if best is None:
                return

            latest_tag, release_data = best
            download_url: Optional[str] = None
            for asset in release_data.get("assets", []):
                if asset.get("name", "").lower().endswith(".exe"):
                    download_url = asset["browser_download_url"]
                    break

            self.update_available.emit(latest_tag, download_url or "")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Download + install (background thread)
    # ------------------------------------------------------------------

    def download_and_install_async(self, download_url: str) -> None:
        t = threading.Thread(
            target=self._download_and_install,
            args=(download_url,),
            daemon=True,
            name="updater-download",
        )
        t.start()

    def _download_and_install(self, url: str) -> None:
        try:
            tmp_path = os.path.join(tempfile.gettempdir(), "TinyType-Update-Setup.exe")

            def _report(block_count, block_size, total_size):
                if total_size > 0:
                    pct = min(100, int(block_count * block_size * 100 / total_size))
                    self.download_progress.emit(pct)

            urllib.request.urlretrieve(url, tmp_path, reporthook=_report)
            self._installer_path = tmp_path
            self.download_finished.emit(tmp_path)
        except Exception:
            pass

    def launch_installer(self) -> None:
        """Launch the downloaded installer silently and quit the app."""
        if self._installer_path and os.path.exists(self._installer_path):
            subprocess.Popen([self._installer_path, "/SILENT"])

    # ------------------------------------------------------------------
    # Version comparison  (PEP 440 / semver aware)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse(v: str):
        """
        Return a comparable object for version string v.
        Handles:  1.0.0  1.0.0b1  1.0.0-beta.1  1.0.0-rc.2  1.0.0.post1
        Uses packaging.version if available, otherwise a simple fallback.
        """
        # Normalise semver pre-release separators to PEP 440 style:
        # 1.0.0-beta.1  ->  1.0.0b1
        # 1.0.0-rc.2    ->  1.0.0rc2
        # 1.0.0-alpha.3 ->  1.0.0a3
        import re
        v = v.strip()
        v = re.sub(r"-beta\.?(\d*)", lambda m: f"b{m.group(1) or '0'}", v)
        v = re.sub(r"-alpha\.?(\d*)", lambda m: f"a{m.group(1) or '0'}", v)
        v = re.sub(r"-rc\.?(\d*)", lambda m: f"rc{m.group(1) or '0'}", v)
        v = v.lstrip("v")

        try:
            from packaging.version import Version
            return Version(v)
        except Exception:
            pass

        # Fallback: strip non-numeric suffix and compare numerically
        nums = re.match(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?", v)
        if nums:
            return tuple(int(x or 0) for x in nums.groups())
        return (0,)

    @staticmethod
    def _is_prerelease(v: str) -> bool:
        import re
        v = v.lstrip("v").lower()
        try:
            from packaging.version import Version
            return Version(v).is_prerelease
        except Exception:
            return bool(re.search(r"(alpha|beta|rc|a\d|b\d)", v))

    @classmethod
    def _is_newer(cls, latest: str, current: str) -> bool:
        return cls._parse(latest) > cls._parse(current)
