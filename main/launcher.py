#!/usr/bin/python
#The above is a shebang for executing on Mac/Linux systems (must use chmod +x filname.py and execute using ./filename.py)

import functions
#I've split functions off into a different script for ease of editing/adding new levels/resolutions etc
import subprocess
#subprocess allows us to open a new window and close the old window when we change the resolution (which enables us to run the game on different computers)
import sys
#we use sys for reading/editing a hidden settings file for saving preferences
import pygame
#pygame gives us easy graphics toys
import level1, level2, level3, level4
#I've split the levels off into different scripts for ease of adding/changing them

pygame.mixer.pre_init(44100, -16, 2, 2048)
#this sets the system audio settings so that our game plays audio at the right speed
pygame.init()
#this gets pygame ready to start displaying things

resolution = functions.get_resolution()
#calls our get_resolution function in the functions script which reads the desired resolution from a hidden preferences file (or creates that file with a default resolution if the file hasn't been made yet)

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
#defines the colours white and black for white text and to clear the screen of old images

difficulty = 7
#this is set at this screen so that we have have editable difficulty levels in the future
#it is essentially the maximum horizontal/vertical speed that the craft can survive landing at

resource_location = functions.resource("location", resolution)
#tells the program where to find our graphics depending on the desired resolution (as changing the res of the graphics each time slows the game down too much)

icon = pygame.image.load(resource_location+"player_l.png")
#loads up the application icon from the resources folder
pygame.display.set_icon(icon)
#tells pygame to use the previously loaded application icon as the application icon
screen = pygame.display.set_mode(resolution)
#sets the screen size to that defined by the resolution that is in the hidden settings file
pygame.display.set_caption("Lander")
#sets the title of the window to "Lander"
background_image = pygame.image.load(resource_location+"launcher.jpg")
#loads up a splash-screen background image from the relevant resolution resources folder
screen.fill(BLACK)
#clears the screen
screen.blit(background_image, [0,0])
#displays the background image on the screen

clock = pygame.time.Clock()
#gives us a steady time (for playing music and counting frames per second)
pygame.mixer.music.load("../resources/title_sound.mp3")
#loads up the background music
pygame.mixer.music.play(-1)
#gets the background music playing on loop

large_font = pygame.font.SysFont('Courier New', functions.resource("large_font", resolution), True, False)
#defines the font for pygame to use for large things, using sizes in the functions file so that it obeys resoultion changes
medium_font = pygame.font.SysFont('Courier New', functions.resource("med_font", resolution), True, False)
#same as above but for medium fonts
small_font = pygame.font.SysFont('Courier New', functions.resource("small_font", resolution), True, False)
#same as above but for small fonts

title_text = large_font.render("Lander", True, WHITE)
#renders the title text
subtitle_text = medium_font.render("An educational physics game", True, WHITE)
#renders the subtitle text
mute_text = small_font.render("Toggle Mute [M]", True, WHITE)
#renders the text that gives the player the option to mute music
display_text = small_font.render("Toggle Screen Resolution [R]", True, WHITE)
#renders the text that gives the player the option to change the screen resolution
exit_text = small_font.render("Exit [ESC]", True, WHITE)
#renders the text that tells the player how to exit
play_text = medium_font.render("Press [SPACE] to Start", True, WHITE)
#renders the text that tells the player how to start playing

class Buttons(pygame.sprite.Sprite):
    """This code creates a sprites class to allow the showing of mute/resolution/exit buttons"""
    def __init__(self):
        super(Buttons, self).__init__()

        self.image = ""
        self.xy_location = ""
        #creates two empty properties that the buttons use

sprite_list = pygame.sprite.Group()
#initialize a list of sprites that need to be displayed on the screen

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
                    #next_level = level2.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                    #if next_level == True:
                        #next_level = level3.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                        #if next_level == True:
                            #next_level = level4.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                            #etc etc
                    pass #do nothing (remove when levels are added)

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
