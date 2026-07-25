# non-safe code to make statements unskipable for several seconds
#
# by lolbot (lolbot_iichan@mail.ru)
# iichan.ru, 2012
#
# Web/WASM has no threading -- use a no-op there.

init -100 python:

    if renpy.emscripten:
        class ThreadedSkipDisabler(object):
            def __init__(self, timeout_sec):
                pass
    else:
        real_map_event = renpy.display.behavior.map_event
        def my_map_event(ev, name):
            if real_map_event(ev, "skip"):
                renpy.config.skipping = "slow"
            if renpy.display.behavior.map_keyup(ev, "skip"):
                renpy.config.skipping = None
            return False
        real_renpy_run = renpy.display.behavior.run
        my_renpy_run   = lambda name: True

        def nonsafe_noskip_mode():
            renpy.display.behavior.map_event = my_map_event
            renpy.display.behavior.run       = my_renpy_run
            renpy.config.allow_skipping      = False

        def nonsafe_skip_mode():
            renpy.display.behavior.map_event = real_map_event
            renpy.display.behavior.run       = real_renpy_run
            renpy.config.allow_skipping      = True

        import threading
        import time

        class ThreadedSkipDisabler(object):
            def __init__(self,timeout_sec):
                self.timeout_sec = timeout_sec
                self.preload_thread = threading.Thread(target=self.run, name="waiter")
                self.preload_thread.start()

            def run(self):
                global nonsafe_noskip_mode
                global nonsafe_skip_mode
                sec_start = time.time()
                nonsafe_noskip_mode()
                while time.time() - sec_start < self.timeout_sec:
                    time.sleep(1)
                nonsafe_skip_mode()
