# Web: browsers block unmuted media until a user gesture.
# Show a click gate before splash video so opening.webm has sound.

init python:
    def _web_unlock_audio():
        if not renpy.emscripten:
            return
        try:
            import emscripten
            emscripten.run_script(
                "(function(){"
                "try{if(typeof renpyAudio!=='undefined'&&renpyAudio.unpauseAllAtStart){renpyAudio.unpauseAllAtStart();}}"
                "catch(e){}"
                "try{var AC=window.AudioContext||window.webkitAudioContext;"
                "if(AC){window.__renpyUnlockAC=window.__renpyUnlockAC||new AC();"
                "window.__renpyUnlockAC.resume();}}"
                "catch(e){}"
                "})();"
            )
        except Exception:
            pass


screen web_audio_unlock():
    modal True
    zorder 1000

    button:
        xfill True
        yfill True
        background "#000000"
        action [Function(_web_unlock_audio), Return()]

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 16

            text "欢迎来到鄂木斯克":
                xalign 0.5
                size 36
                color "#f0f0f0"
                text_align 0.5

            text "点击开始":
                xalign 0.5
                size 28
                color "#cccccc"
                text_align 0.5

            text "Click to start":
                xalign 0.5
                size 20
                color "#888888"
                text_align 0.5
