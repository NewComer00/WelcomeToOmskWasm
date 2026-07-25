init:

    image animation:
        "art/0.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/1.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/2.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/3.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/4.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/5.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/6.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/7.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/8.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/9.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/10.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/11.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/12.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/13.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/14.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/15.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/16.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/17.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/18.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/19.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/20.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/21.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/22.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0
        pause 6
        linear 2.0 alpha 0.0
        "art/23.jpg"
        alpha 0.0
        linear 2.0 alpha 1.0

label ending:
    
    $ ThreadedSkipDisabler(2)

    scene black with fade

    if not persistent.seen_ending:
        $ persistent.seen_ending = True

    play music "OUTRO.mp3" fadein 1 fadeout 1
    show animation
    $ renpy.pause(324)
    return
