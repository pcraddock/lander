import pygame
#we need pygame for fonts
import math
#we need pythons math library for absolute value functions for safe landing calculations

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)
RED    = (255,   0,   0)
ORANGE = (255, 127,   0)
#RGB colour definitions for text

def get_resolution():
    """function that reads a hidden .settings.txt file where the resolution preferences are stored (we can store other preferences here later)"""
    try:
        #runs if the file exists
        file = open("../resources/.settings.txt", "r")
        contents = file.read()
        if contents == "1920x1080":
            resolution = [1920, 1080]
        elif contents == "1280x720":
            resolution = [1280, 720]
        file.close()
    except:
        #runs if the file doesn't exist
        file = open("../resources/.settings.txt", "w")
        file.write("1920x1080")
        file.close()
        resolution = [1920, 1080]
    return resolution

def toggle_resolution():
    if get_resolution() == [1920, 1080]:
        writ = "1280x720"
        resolution = [1280, 720]
    elif get_resolution() == [1280, 720]:
        writ = "1920x1080"
        resolution = [1920, 1080]
    file = open("../resources/.settings.txt", "w")
    file.write(writ)
    file.close()
    return resolution, "../resources/"+writ+"/"

def safe_landing(player, difficulty):
    if math.fabs(player.velocities[0]) <= difficulty and math.fabs(player.velocities[1]) <= difficulty:
        return True
    else:
        return False

def surface_collision(screen, resolution, player, difficulty):
    font = pygame.font.SysFont('Courier New', resource("med_font", resolution), True, False)
    success_text = font.render("Good Landing, Captain!", True, GREEN)
    next_level_text = font.render("Press [SPACE] to try the next level.", True, GREEN)
    crash_text = font.render("You came in too fast, Captain!", True, RED)
    instruct_text = font.render("Press [A] to play again.", True, WHITE)
    exit_text = font.render("Press [ESC] to exit.", True, WHITE)

    if safe_landing(player, difficulty) == True:
        #If landing is safe display success messages
        screen.blit(success_text, resource("success", resolution))
        screen.blit(instruct_text, resource("instruct", resolution))
        screen.blit(exit_text, resource("exit_text", resolution))
        screen.blit(next_level_text, resource("next_level", resolution))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to True
        safe_landing_check = True
        playing = False
    else:
        #If landing is crash, display try again messages
        player.explosion_sound.play()
        screen.blit(crash_text, resource("crash", resolution))
        screen.blit(instruct_text, resource("instruct", resolution))
        screen.blit(exit_text, resource("exit_text", resolution))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to False
        safe_landing_check = False
        playing = False

    return player, safe_landing_check, playing

def resource(thing, res):
    high_res = {
    "location" : "../resources/1920x1080/",
    "large_font" : 150,
    "med_font" : 50,
    "small_font" : 30,
    "audio_icon" : [10, 10],
    "res_icon" : [660, 10],
    "title" : [675, 175],
    "subtitle" : [530, 325],
    "mute" : [90, 25],
    "display" : [750, 25],
    "exit" : [1700, 25],
    "play" : [620, 675],
    "success" : [630, 150],
    "crash" : [500, 150],
    "instruct" : [590, 250],
    "exit_text" : [660, 325],
    "next_level" : [450, 550],
    "init_velocity" : [6, 3],
    "init_position" : [105, 75],
    "x_vel_txt" : [15, 15],
    "y_vel_txt" : [15, 45],
    "fuel_txt" : [15, 75],
    "planet_tag" : [15, 105],
    "frame_rate_txt" : [15, 105],
    "drag_txt_x" : [15, 135],
	"drag_txt_y" : [15,165],
    }

    low_res = {
    "location" : "../resources/1280x720/",
    "large_font" : 100,
    "med_font" : 33,
    "small_font" : 20,
    "audio_icon" : [7, 7],
    "res_icon" : [440, 7],
    "title" : [450, 117],
    "subtitle" : [353, 217],
    "mute" : [60, 17],
    "display" : [500, 17],
    "exit" : [1133, 17],
    "play" : [413, 450],
    "success" : [420, 100],
    "crash" : [333, 100],
    "instruct" : [403, 167],
    "exit_text" : [447, 217],
    "next_level" : [303, 367],
    "init_velocity" : [2, 1],
    "init_position" : [70, 50],
    "x_vel_txt" : [10, 10],
    "y_vel_txt" : [10, 30],
    "fuel_txt" : [10, 50],
    "planet_tag" : [10, 70],
    "frame_rate_txt" : [10, 90],
	"drag_txt_x" : [10, 110],
	"drag_txt_y" : [10,130],
    }

    if res == [1280, 720]:
        ret = low_res[thing]
    elif res == [1920, 1080]:
        ret = high_res[thing]
    return ret
