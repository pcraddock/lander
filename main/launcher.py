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

audio_on = Buttons()
#makes a button called audio_on
audio_on.image = pygame.image.load(resource_location+"unmuted.png")
#defines the image used for the button
audio_on.xy_location = functions.resource("audio_icon", resolution)
#defines where the button will appear
sprite_list.add(audio_on)
#adds the button to the list of sprites to display

audio_off = Buttons()
#makes a button called audio_off
audio_off.image = pygame.image.load(resource_location+"muted.png")
#defines the image used for the button
audio_off.xy_location = functions.resource("audio_icon", resolution)
#defines where the button will appear
sprite_list.add(audio_off)
#adds the button to the list of sprites to display

low_res = Buttons()
#makes a button called low_res
low_res.image = pygame.image.load(resource_location+"low_res.png")
#defines the image used for the button
low_res.xy_location = functions.resource("res_icon", resolution)
#defines where the button will appear
sprite_list.add(low_res)
#adds the button to the list of sprites to display

high_res = Buttons()
#makes a button called high_res
high_res.image = pygame.image.load(resource_location+"high_res.png")
#defines the image used for the button
high_res.xy_location = low_res.xy_location = functions.resource("res_icon", resolution)
#defines where the button will appear
sprite_list.add(high_res)
#adds the button to the list of sprites to display

audio_state = True
#a variable used to define whether the music is on or off by default

done = False
while not done:
    #enables quitting of the game using esc
    for event in pygame.event.get():
        #checks for events (e.g. clicking things, pressing keys)
        if event.type == pygame.QUIT:
            #checks to see if the x in the corner of the window was pressed
            done = True
            #drops out of the loop if it has been
        elif event.type == pygame.KEYDOWN:
            #checks to see if a keyboard button was pressed
            if event.key == pygame.K_ESCAPE:
                #checks to see if ESC was pressed
                done = True
                #drops out of the loop if it has been
            elif event.key == pygame.K_r:
                #checks to see if the "r" key was pressed
                resolution, resource_location = functions.toggle_resolution()
                #calls a function to change the resolution in the hidden settings file
                subprocess.Popen("python launcher.py")
                #launches a new instance of the game which will read the new resolution from the hidden settings file
                done = True
                #closes the current instance of the game by dropping out of the loop
            elif event.key == pygame.K_m:
                #checks to see if the "m" key was pressed
                if audio_state == True:
                    #checks to see if the music is on
                    audio_state = False
                    #changes the audio state variable for future reference
                    pygame.mixer.music.pause()
                    #pauses the music
                elif audio_state == False:
                    #checks to see if the music is off
                    audio_state = True
                    #changes the audio state variable for future reference
                    pygame.mixer.music.unpause()
                    #unpauses the music
            elif event.key == pygame.K_SPACE:
                #checks to see if the space key was pressed
                next_level = level1.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                #if it was then run the next level (the code here will wait until the level is completed then drop back in)
                if next_level == True:
                    #if it is completed successfully then run the next level (uncomment when built)
                    #next_level = level2.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                    #if next_level == True:
                        #next_level = level3.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                        #if next_level == True:
                            #next_level = level4.play(screen, clock, difficulty, audio_state, resource_location, resolution)
                            #etc etc
                    pass #do nothing (remove when levels are added)

    if audio_state == True:
        #checks to see if the current audio state is on
        screen.blit(audio_on.image, audio_on.xy_location)
        #prints the audio on button on the screen
    elif audio_state == False:
        #checks to see if the current audio state is off
        screen.blit(audio_off.image, audio_off.xy_location)
        #prints the audio off button on the screen
    if resolution == [1920, 1080]:
        #checks to see if the current resolution is high
        screen.blit(high_res.image, high_res.xy_location)
        #prints the high resolution button on the screen
    elif resolution == [1280, 720]:
        #checks to see if the current resolution is low
        screen.blit(low_res.image, low_res.xy_location)
        #prints the low resolution button on the screen


    #print on the screen the text that appears on the title screen
    screen.blit(title_text, functions.resource("title", resolution))
    screen.blit(subtitle_text, functions.resource("subtitle", resolution))
    screen.blit(mute_text, functions.resource("mute", resolution))
    screen.blit(display_text, functions.resource("display", resolution))
    screen.blit(exit_text, functions.resource("exit", resolution))
    screen.blit(play_text, functions.resource("play", resolution))

    clock.tick(30)
    #essentially defines the maximum frame rate whilst keeping CPU usage low; frame rate may still be way lower than this
    pygame.display.flip()
    #"flip" the display i.e. take what's been "blit"ed and display it to the user
    screen.fill(BLACK)
    #cover up the last stuff on the screen
    screen.blit(background_image, [0,0])
    #write the background image to the screen for the next pass

pygame.quit()
#quits the game
