# WelcomeToOmskWasm

[中文](README.md) | English

Unofficial Ren'Py Web port of
*Добро пожаловать в Омск / Welcome to Omsk* (2012), with a Chinese language
patch.

Copyright in the original work belongs to Связной и Семён. This repository is a
non-commercial fan project and is not affiliated with the original authors.
Read [NOTICE.md](NOTICE.md) before use.

## Play online

<https://newcomer00.github.io/WelcomeToOmskWasm/>

Desktop Chrome / Edge / Firefox recommended. The site is built and deployed to
`gh-pages` by GitHub Actions.

## Repository layout

- `game/` — project source and assets (including Chinese text in `chinese.rpt`)
- `progressive_download.txt` — Web progressive-download rules
- `scripts/ci_web_build.py` — fetch the SDK and build the Web package into `_site/`
- `scripts/web_cli.rpy` — CLI `web_build` shim for Ren'Py 7.6.3
- `.github/workflows/` — Pages deploy workflow

`game.zip` and the full site are not kept on `main`; they exist only as CI
artifacts and on `gh-pages`.

## Local build

### Option 1: build script

Requires Python 3. The first run downloads Ren'Py 7.6.3 SDK and Web support into
`.renpy-sdk/` (gitignored).

Linux / macOS:

```bash
python3 scripts/ci_web_build.py
cd _site
python3 -m http.server 8000
```

Windows:

```bat
py -3 scripts\ci_web_build.py
cd _site
py -3 -m http.server 8000
```

Then open <http://127.0.0.1:8000/> in a browser. Do not open `index.html`
directly.

> On Linux, if placeholder image generation fails, install `xvfb`; the script
> will use `xvfb-run` when available.

Optional environment variables:

- `SDK_DIR` — SDK location
- `SITE_DIR` — output directory
- `RENPY_VERSION` — Ren'Py version

### Option 2: local Ren'Py install

If you already have Ren'Py 7.6.3 and have extracted `renpy-*-web.zip`, copy
`scripts/web_cli.rpy` into the SDK `launcher/game/` directory (once), then run:

Linux / macOS:

```bash
/path/to/renpy-sdk/renpy.sh launcher web_build "$(pwd)" --destination _site
```

Windows:

```bat
C:\path\to\renpy-sdk\renpy.exe launcher web_build "%CD%" --destination _site
```

## Desktop

Install [Ren'Py 7.6+](https://www.renpy.org/), add this directory to Projects,
and launch.

## Language

The main menu can switch between Chinese and Русский. Chinese text lives in
`game/chinese.rpt`.

## License

- Script, images, audio, and video of the original belong to their authors;
  this project is for non-commercial fan use only
- Ren'Py / Ren'Py Web are under their own licenses
- See [NOTICE.md](NOTICE.md) for the translation and adaptation scripts
