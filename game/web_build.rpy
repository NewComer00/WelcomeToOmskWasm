# Build / web packaging metadata for Ren'Py 7

define config.name = "Welcome to Omsk"
define config.version = "2012-zh-web"
define build.name = "WelcomeToOmsk"
define build.version = "2012.zh.web"

# Web/mobile: Movie(channel='movie') raises if hw_video is true.
define config.hw_video = False

# Web video (webaudio) only works with gl2/gles2 — not the legacy gles renderer.
define config.gl2 = True

init -1500 python:
    # Persistent from an earlier web run can force gles and kill video.
    if renpy.emscripten:
        persistent._gl2 = True
        if preferences.renderer in ("gles", "gl", "sw", "angle"):
            preferences.renderer = "auto"

init python:
    # Keep AVI out of packages (WebM used instead); exclude subtitle sources/docs noise.
    build.classify("game/**.avi", None)
    build.classify("game/**.ass", None)
    build.classify("game/**.srt", None)
    build.classify("**~", None)
    build.classify("**/#*#", None)
    build.classify("**/thumbs.db", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.documentation("*.html")
    build.documentation("*.txt")
    build.documentation("*.md")
