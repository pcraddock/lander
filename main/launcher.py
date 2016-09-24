#!/usr/bin/python

import functions, subprocess, sys, pygame, level1, level2, level3, level4

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

resolution = functions.get_resolution()

#initialize colours
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

#initialize other stuff
difficulty = 7

screen_width, screen_height = resolution
resource_location = functions.resource("location", resolution)

#initialize screen stuff
icon = pygame.image.load(resource_location+"player_l.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Lander")
background_image = pygame.image.load(resource_location+"launcher.jpg")
screen.fill(BLACK)
screen.blit(background_image, [0,0])
clock = pygame.time.Clock()

#initialize audio stuff
pygame.mixer.music.load("../resources/title_sound.mp3")
pygame.mixer.music.play(-1)

#initialize text stuff
large_font = pygame.font.SysFont('Courier New', functions.resource("large_font", resolution), True, False)
medium_font = pygame.font.SysFont('Courier New', functions.resource("med_font", resolution), True, False)
small_font = pygame.font.SysFont('Courier New', functions.resource("small_font", resolution), True, False)
title_text = large_font.render("Lander", True, WHITE)
subtitle_text = medium_font.render("An educational physics game", True, WHITE)
mute_text = small_font.render("Toggle Mute [M]", True, WHITE)
display_text = small_font.render("Toggle Screen Resolution [R]", True, WHITE)
exit_text = small_font.render("Exit [ESC]", True, WHITE)
play_text = medium_font.render("Press [SPACE] to Start", True, WHITE)

#initialize a class for the selection sprites
class Buttons(pygame.sprite.Sprite):
    """A child class of sprites to describe the launcher buttons"""
    def __init__(self):
        super(Buttons, self).__init__()

        self.image = ""
        self.xy_location = ""

#initialize a list of sprites
sprite_list = pygame.sprite.Group()

#initialize the sprites for the buttons
audio_on = Buttons()
audio_on.image = pygame.image.load(resource_location+"unmuted.png")
audio_on.xy_location = functions.resource("audio_icon", resolution)
sprite_list.add(audio_on)

audio_off = Buttons()
audio_off.image = pygame.image.load(resource_location+"muted.png")
audio_off.xy_location = functions.resource("audio_icon", resolution)
sprite_list.add(audio_off)

low_res = Buttons()
low_res.image = pygame.image.load(resource_location+"low_res.png")
low_res.xy_location = functions.resource("res_icon", resolution)
sprite_list.add(low_res)

high_res = Buttons()
high_res.image = pygame.image.load(resource_location+"high_res.png")
high_res.xy_location = low_res.xy_location = functions.resource("res_icon", resolution)
sprite_list.add(high_res)

#initialize some default settings
audio_state = True #on

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_r:
                resolution, resource_location = functions.toggle_resolution()
                subprocess.Popen("python launcher.py")
                done = True
            elif event.key == pygame.K_m:
                if audio_state == True:
                    audio_state = False
                    pygame.mixer.music.pause()
                elif audio_state == False:
                    audio_state = True
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_SPACE:
                next_level = level1.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                if next_level == True:
                    next_level = level2.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                    if next_level == True:
                        next_level = level3.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                        if next_level == True:
                            next_level = level4.play(screen, clock, difficulty, audio_state, resource_location, resolution)

    if audio_state == True:
        screen.blit(audio_on.image, audio_on.xy_location)
    elif audio_state == False:
        screen.blit(audio_off.image, audio_off.xy_location)
    if resolution == [1920, 1080]:
        screen.blit(high_res.image, high_res.xy_location)
    elif resolution == [1280, 720]:
        screen.blit(low_res.image, low_res.xy_location)


    #load the title text
    screen.blit(title_text, functions.resource("title", resolution))
    screen.blit(subtitle_text, functions.resource("subtitle", resolution))
    screen.blit(mute_text, functions.resource("mute", resolution))
    screen.blit(display_text, functions.resource("display", resolution))
    screen.blit(exit_text, functions.resource("exit", resolution))
    screen.blit(play_text, functions.resource("play", resolution))

    #finally set frame rate and flip the display
    clock.tick(40)
    pygame.display.flip()
    screen.fill(BLACK)
    screen.blit(background_image, [0,0])

pygame.quit()
