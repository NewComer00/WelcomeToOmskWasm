# WelcomeToOmskWasm

《Добро пожаловать в Омск / Welcome to Omsk》（2012）的非官方 Ren'Py Web 移植，附中文补丁。

原作版权归 Связной и Семён 所有。本仓库为非商业粉丝项目，与原作者无关，使用前请阅读 [NOTICE.md](NOTICE.md)。

## 在线试玩

https://newcomer00.github.io/WelcomeToOmskWasm/

建议使用桌面版 Chrome / Edge / Firefox。站点由 GitHub Actions 自动构建部署至 `gh-pages`。

## 仓库结构

- `game/` — 工程源码与资源（含中文文本 `chinese.rpt`）
- `progressive_download.txt` — Web 渐进下载规则
- `ci/web_cli.rpy` — 为 Ren'Py 7.6.3 补充 `web_build` 命令行支持
- `scripts/ci_web_build.py` — 拉取 SDK 并构建 Web 包，输出至 `_site/`
- `.github/workflows/` — Pages 部署流程

`game.zip` 及完整站点内容不纳入 `main` 分支，仅在 CI 构建产物与 `gh-pages` 中生成。

## 本地构建

### 方式一：构建脚本

需要 Python 3。首次运行会自动下载 Ren'Py 7.6.3 SDK 及 Web 打包组件至 `.renpy-sdk/`（已加入 .gitignore）。

Linux / macOS：

```bash
python3 scripts/ci_web_build.py
cd _site
python3 -m http.server 8000
```

Windows：

```bat
py -3 scripts\ci_web_build.py
cd _site
py -3 -m http.server 8000
```

构建完成后请通过浏览器访问 http://127.0.0.1:8000/，不要直接打开 `index.html`。

> Linux 环境如遇图片占位生成失败，请安装 `xvfb`，脚本会自动通过 `xvfb-run` 调用。

支持的环境变量（可选）：
- `SDK_DIR` — SDK 存放路径
- `SITE_DIR` — 输出目录
- `RENPY_VERSION` — 指定 Ren'Py 版本

### 方式二：本地已安装的 Ren'Py

若本机已安装 Ren'Py 7.6.3 并解压 `renpy-*-web.zip`，可将 `ci/web_cli.rpy` 拷贝至 SDK 的 `launcher/game/` 目录（仅需一次），随后执行：

Linux / macOS：

```bash
/path/to/renpy-sdk/renpy.sh launcher web_build "$(pwd)" --destination _site
```

Windows：

```bat
C:\path\to\renpy-sdk\renpy.exe launcher web_build "%CD%" --destination _site
```

## 桌面端运行

安装 [Ren'Py 7.6+](https://www.renpy.org/)，将本目录添加至 Projects 列表后即可启动。

## 语言切换

主菜单支持中文 / Русский 切换，中文文本位于 `game/chinese.rpt`。

## 许可

- 原作剧本、图像、音视频版权归原作者所有，本项目仅供粉丝非商业用途
- Ren'Py / Ren'Py Web 遵循其自身许可协议
- 汉化及适配脚本的许可信息见 [NOTICE.md](NOTICE.md)
