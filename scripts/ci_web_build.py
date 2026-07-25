#!/usr/bin/env python3
"""Download Ren'Py SDK + web support, build this project, write to _site/."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parent.parent
SDK_DIR = Path(os.environ.get("SDK_DIR", ROOT / ".renpy-sdk"))
SITE_DIR = Path(os.environ.get("SITE_DIR", ROOT / "_site"))
RENPY_VERSION = os.environ.get("RENPY_VERSION", "7.6.3")

BASE = f"https://www.renpy.org/dl/{RENPY_VERSION}"
WEB_URL = f"{BASE}/renpy-{RENPY_VERSION}-web.zip"


def sdk_archive_url() -> str:
    # zip has renpy.exe (Windows); tar.bz2 is enough on Linux/macOS CI.
    if sys.platform == "win32":
        return f"{BASE}/renpy-{RENPY_VERSION}-sdk.zip"
    return f"{BASE}/renpy-{RENPY_VERSION}-sdk.tar.bz2"


def download(url: str, dest: Path) -> None:
    print(f"Downloading {url} ...")
    dest.parent.mkdir(parents=True, exist_ok=True)

    def _progress(block_num: int, block_size: int, total: int) -> None:
        if total <= 0:
            return
        done = min(block_num * block_size, total)
        pct = done * 100 // total
        if block_num % 50 == 0 or done >= total:
            print(f"\r  {pct:3d}% ({done // (1024 * 1024)} / {total // (1024 * 1024)} MiB)", end="")
            if done >= total:
                print()

    urlretrieve(url, dest, _progress)


def _members_strip_one(names):
    """Yield archive member names under a single top-level directory, stripped."""
    tops = {n.split("/", 1)[0] for n in names if n and not n.startswith(".")}
    tops = {t for t in tops if t}
    if len(tops) != 1:
        return None
    prefix = tops.pop() + "/"
    return prefix


def extract_archive(archive: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    if archive.suffix == ".zip" or archive.name.endswith(".zip"):
        with zipfile.ZipFile(archive) as zf:
            names = zf.namelist()
            prefix = _members_strip_one(names)
            if prefix is None:
                zf.extractall(dest)
                return
            for info in zf.infolist():
                name = info.filename
                if not name.startswith(prefix):
                    continue
                rel = name[len(prefix) :]
                if not rel:
                    continue
                out = dest / rel
                if name.endswith("/"):
                    out.mkdir(parents=True, exist_ok=True)
                else:
                    out.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(info) as src, open(out, "wb") as dst:
                        shutil.copyfileobj(src, dst)
        return

    # .tar.bz2 / .tar.gz / etc.
    with tarfile.open(archive, "r:*") as tf:
        members = tf.getmembers()
        prefix = _members_strip_one([m.name for m in members])
        extract_kw = {}
        if sys.version_info >= (3, 12):
            extract_kw["filter"] = "data"
        if prefix is None:
            tf.extractall(dest, **extract_kw)
            return
        for member in members:
            if not member.name.startswith(prefix):
                continue
            member.name = member.name[len(prefix) :]
            if member.name:
                tf.extract(member, dest, **extract_kw)


def find_renpy(sdk: Path) -> Path | None:
    candidates = []
    if sys.platform == "win32":
        candidates = [sdk / "renpy.exe", sdk / "renpy.bat"]
    else:
        candidates = [sdk / "renpy.sh"]
    for c in candidates:
        if c.is_file():
            return c
    for c in (sdk / "renpy.exe", sdk / "renpy.sh"):
        if c.is_file():
            return c
    return None


def ensure_sdk() -> Path:
    SDK_DIR.mkdir(parents=True, exist_ok=True)
    existing = find_renpy(SDK_DIR)
    if existing is not None:
        return existing

    url = sdk_archive_url()
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / Path(url).name
        download(url, archive)
        print(f"Extracting SDK into {SDK_DIR} ...")
        extract_archive(archive, SDK_DIR)

    renpy = find_renpy(SDK_DIR)
    if renpy is None:
        raise SystemExit(f"Ren'Py launcher not found under {SDK_DIR}")
    return renpy


def ensure_web() -> None:
    marker = SDK_DIR / "web" / "index.html"
    if marker.is_file():
        return
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "renpy-web.zip"
        download(WEB_URL, archive)
        print(f"Extracting web support into {SDK_DIR} ...")
        # Archive top-level is usually "web/"
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(SDK_DIR)
    if not marker.is_file():
        raise SystemExit(f"Expected {marker} after extracting web.zip")


def install_web_cli() -> None:
    src = ROOT / "ci" / "web_cli.rpy"
    if not src.is_file():
        raise SystemExit(f"Missing {src}")
    dest = SDK_DIR / "launcher" / "game" / "web_cli.rpy"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def run_web_build(renpy: Path) -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(renpy),
        "launcher",
        "web_build",
        str(ROOT),
        "--destination",
        str(SITE_DIR),
    ]

    # Placeholder image generation may need a display on Linux CI.
    if sys.platform.startswith("linux") and shutil.which("xvfb-run"):
        cmd = ["xvfb-run", "-a", *cmd]

    print("Building web package...")
    print(" ", " ".join(cmd))
    # renpy.sh expects to be started from the SDK directory.
    subprocess.run(cmd, cwd=str(SDK_DIR), check=True)


def finalize_site() -> None:
    index = SITE_DIR / "index.html"
    game_zip = SITE_DIR / "game.zip"
    if not index.is_file() or not game_zip.is_file():
        raise SystemExit(f"Build incomplete under {SITE_DIR}")

    (SITE_DIR / ".nojekyll").touch()
    notice = ROOT / "NOTICE.md"
    if notice.is_file():
        shutil.copy2(notice, SITE_DIR / "NOTICE.md")

    site_size = sum(p.stat().st_size for p in SITE_DIR.rglob("*") if p.is_file())
    zip_size = game_zip.stat().st_size
    print(f"Site ready: {SITE_DIR}")
    print(f"  _site:   {site_size / (1024 * 1024):.1f} MiB")
    print(f"  game.zip:{zip_size / (1024 * 1024):.1f} MiB")


def main() -> None:
    renpy = ensure_sdk()
    ensure_web()
    install_web_cli()
    run_web_build(renpy)
    finalize_site()


if __name__ == "__main__":
    main()
