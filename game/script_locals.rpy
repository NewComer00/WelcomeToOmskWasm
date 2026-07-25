
label locals:

    $ ThreadedSkipDisabler(2)

    if not persistent.seen_locals:
        $ persistent.seen_locals = True
    $ renpy.movie_cutscene("locals.webm")
    return
