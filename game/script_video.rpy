init:
    image scp087 = "scp087.png"
    image tv = "tv.png"
    # Avoid default channel "movie" — blocked on web/mobile when hw_video is true.
    image movie = Movie(size=(320, 240), xalign=0.5, yalign=0.5, channel="movie_display")

    image clean:
        "noise.png"
        alpha 0.05
    image noise:
        "noise.png"
        alpha 0.15
    image noise_bird:
        "noise_bird.png"
        alpha 0.25

    image tv_static = anim.SMAnimation("a",
            anim.State("a", "clean"),
            anim.State("b", "noise"),
            anim.State("c", "noise_bird"),
            anim.Edge("b", 0.5, "a", prob=5, trans=Dissolve(0.5, alpha=True)),
            anim.Edge("b", 0.5, "b"),
            anim.Edge("c", 0.5, "a", prob=5, trans=Dissolve(0.5, alpha=True)),
            anim.Edge("c", 0.5, "c"),
            anim.Edge("a", 0.5, "a", prob=100),
            anim.Edge("a", 0.5, "b", prob=10, trans=Dissolve(0.5, alpha=True)),
            anim.Edge("a", 0.5, "c", trans=Dissolve(0.5, alpha=True)),
        )

label video:

    $ ThreadedSkipDisabler(2)
    
    if not persistent.seen_video:
        $ persistent.seen_video = True
    $ renpy.music.set_volume(0)
    show scp087 at Position(xpos=205,xanchor=0,ypos=175,yanchor=0)
    show movie at Position(xpos=205,xanchor=0,ypos=175,yanchor=0)
    show tv_static at Position(xpos=205,xanchor=0,ypos=175,yanchor=0)
    show tv at Position(xpos=155,xanchor=0,ypos=125,yanchor=0)
    $ renpy.music.play("VIDEO.webm", channel="movie_display", loop=False)

    $ renpy.pause(206)

    $ renpy.music.stop(channel="movie_display")
    hide movie
    hide tv
    hide tv_static
    hide scp087
    $ renpy.music.set_volume(0.5)
    return
