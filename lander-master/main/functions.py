import pygame
#we need pygame for fonts
import math
#we need pythons math library for absolute value functions for safe landing calculations
import random
#just used for winds

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
        """if contents == "1920x1080":
            resolution = [1920, 1080]"""#SHOULD BE INNECESSARY - TO BE DELETED
        if contents == "1280x720":
            resolution = [1280, 720]
        file.close()
    except:
        #runs if the file doesn't exist
        file = open("../resources/.settings.txt", "w")
        file.write("1280x720")
        file.close()
        resolution = [1280, 720]
    return resolution

"""def toggle_resolution():
    if get_resolution() == [1920, 1080]:
        writ = "1280x720"
        resolution = [1280, 720]
    elif get_resolution() == [1280, 720]:
        writ = "1920x1080"
        resolution = [1920, 1080]
    file = open("../resources/.settings.txt", "w")
    file.write(writ)
    file.close()
    return resolution, "../resources/"+writ+"/" """ #SHOULD BE INNECESSARY

def safe_landing(player, difficulty):
    if math.fabs(player.velocities[0]) <= difficulty and math.fabs(player.velocities[1]) <= difficulty:
        if player.angle <= 10 and player.angle >= -10:
            return True
        else:
            return "angle"
    else:
        return "speed"

def explosion(screen, resolution, player, planet):
    for x in range(0, 5):
        for y in range(0, 5):
            screen.blit(player.explosion_image, (player.rect.topleft[0]-45, player.rect.topleft[1]-30), (x*130, y*130, 130, 130))
            pygame.display.flip()
            screen.blit(planet.bg_image, (0, 0), (0, player.last_altitude, resolution[0], resolution[1]))

def surface_collision(screen, resolution, player, difficulty, planet):
    font = pygame.font.SysFont('Courier New', resource("med_font", resolution), True, False)
    success_text = font.render("Good Landing, Commander!", True, GREEN)
    next_level_text = font.render("Press [SPACE] to try the next level.", True, GREEN)
    crash_text = font.render("You came in too fast, Commander!", True, RED)
    angle_crash_text = font.render("You need to land vertically, Commander!", True, RED)
    instruct_text = font.render("Press [A] to play again.", True, WHITE)
    exit_text = font.render("Press [ESC] to exit.", True, WHITE)

    if safe_landing(player, difficulty) == True:
        #If landing is safe display success messages
        player.landed_sound.play()
        screen.blit(success_text, resource("success", resolution))
        screen.blit(instruct_text, resource("instruct", resolution))
        screen.blit(exit_text, resource("exit_text", resolution))
        screen.blit(next_level_text, resource("next_level", resolution))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to True
        safe_landing_check = True
        playing = False
    elif safe_landing(player, difficulty) == "speed":
        #If landing is crash, display try again messages
        player.explosion_sound.play()
        explosion(screen, resolution, player, planet)
        screen.blit(crash_text, resource("crash", resolution))
        screen.blit(instruct_text, resource("instruct", resolution))
        screen.blit(exit_text, resource("exit_text", resolution))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to False
        safe_landing_check = False
        playing = False
    elif safe_landing(player, difficulty) == "angle":
        #If landing is crash, display try again messages
        player.explosion_sound.play()
        explosion(screen, resolution, player, planet)
        screen.blit(angle_crash_text, resource("angle", resolution))
        screen.blit(instruct_text, resource("instruct", resolution))
        screen.blit(exit_text, resource("exit_text", resolution))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to False
        safe_landing_check = False
        playing = False

    return player, safe_landing_check, playing

def object_collision(screen, resolution, player, difficulty):
    font = pygame.font.SysFont('Courier New', resource("med_font", resolution), True, False)
    success_text = font.render("Good Landing, Commander!", True, GREEN)
    next_level_text = font.render("Press [SPACE] to try the next level.", True, GREEN)
    crash_text = font.render("You can't land on that, Commander!", True, RED)
    instruct_text = font.render("Press [A] to play again.", True, WHITE)
    exit_text = font.render("Press [ESC] to exit.", True, WHITE)

    if safe_landing(player, difficulty) == True:
        #If landing is safe display success messages
        player.landed_sound.play()
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
    """high_res = {
    "location" : "../resources/1920x1080/",
    "large_font" : 150,
    "med_font" : 50,
    "small_font" : 30,
    "audio_icon" : [10, 10],
    "music_icon" : [10, 70],
    "res_icon" : [660, 10],
    "title" : [675, 175],
    "subtitle" : [530, 325],
    "effects" : [90, 25],
    "music" : [90, 85],
    "display" : [750, 25],
    "exit" : [1700, 25],
    "play" : [620, 675],
    "success" : [630, 150],
    "crash" : [500, 150],
    "angle" : [425, 150],
    "instruct" : [590, 250],
    "exit_text" : [660, 325],
    "next_level" : [450, 550],
    "init_velocity" : [9, 9],
    "init_position" : [105, 75],
    "x_vel_txt" : [15, 15],
    "y_vel_txt" : [15, 45],
    "fuel_txt" : [15, 75],
    "planet_tag" : [15, 105],
    "frame_rate_txt" : [15, 105],
    "drag_txt_x" : [15, 135],
	"drag_txt_y" : [15,165],
    "wind_warning" : [15, 195],
    }"""#TO BE DELETED

    low_res = {
    "location" : "../resources/1280x720/",
    "large_font" : 100,
    "med_font" : 33,
    "small_font" : 20,
    "audio_icon" : [7, 7],
    "music_icon" : [7, 47],
    "res_icon" : [440, 7],
    "title" : [450, 117],
    "subtitle" : [353, 217],
    "effects" : [60, 17],
    "music" : [60, 57],
    "display" : [500, 17],
    "exit" : [1133, 17],
    "play" : [413, 450],
    "success" : [420, 100],
    "crash" : [333, 100],
    "angle" : [283, 100],
    "instruct" : [403, 167],
    "exit_text" : [447, 217],
    "next_level" : [303, 367],
    "init_velocity" : [6, 6],
    "init_position" : (int(res[0]/2), int(res[1]/2)),
    "x_vel_txt" : [10, 10],
    "y_vel_txt" : [10, 30],
    "fuel_txt" : [10, 50],
    "planet_tag" : [10, 70],
    "frame_rate_txt" : [10, 90],
	"drag_txt_x" : [10, 110],
	"drag_txt_y" : [10,130],
    "wind_warning" : [10, 150],
    }

    if res == [1280, 720]:
        ret = low_res[thing]
    """elif res == [1920, 1080]:
        ret = high_res[thing]""" #TO BE DELETED
    return ret

def drag(density, velocity, dragCoeff, Area):
	# F = force due to drag
	p = density
	v = velocity
	c = dragCoeff
	A = Area
	if v>0:
		F = 0.5*p*(v**2)*c*A
	elif v<0:
		F = -0.5*p*(v**2)*c*A
	else:
		F=0
	return F

def fix_music(music_state):
    if music_state == True:
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.music.load("../resources/title_sound.mp3")
        pygame.mixer.music.play(-1)
    elif music_state == False:
        pygame.mixer.quit
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.music.load("../resources/title_sound.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

def player_planet_motion(player, planet, screen, resolution):
    player.altitude += player.velocities[1]

    if player.altitude < 0:
        player.rect.center = (player.c_position[0]+int(round(player.velocities[0])), player.c_position[1]+int(round(player.velocities[1])))
        screen.blit(planet.bg_image, [0, 0], (0, 0, resolution[0], resolution[1]))
        screen.blit(planet.map, (resolution[0]-148, 20))
        pygame.draw.rect(screen, WHITE, (resolution[0]-150, 18, 131, 291), 2)
        pygame.draw.rect(screen, ORANGE, (resolution[0]-150, 18, 131, 76), 2)
        player.c_position = player.rect.center
    elif player.altitude <= resolution[1]*3:
        screen.blit(planet.bg_image, [0, 0], (0, player.altitude, resolution[0], resolution[1]))
        screen.blit(planet.map, (resolution[0]-148, 20))
        pygame.draw.rect(screen, WHITE, (resolution[0]-150, 18, 131, 291), 2)
        pygame.draw.rect(screen, ORANGE, (resolution[0]-150, int(player.altitude/10)+18, 131, 76), 2)
        player.rect.center = (player.c_position[0]+int(round(player.velocities[0])), player.c_position[1])
        player.c_position = player.rect.center
        player.last_altitude = player.altitude
    else:
        player.rect.center = (player.c_position[0]+int(round(player.velocities[0])), player.c_position[1]+int(round(player.velocities[1])))
        screen.blit(planet.bg_image, [0, 0], (0, player.last_altitude, resolution[0], resolution[1]))
        screen.blit(planet.map, (resolution[0]-148, 20))
        pygame.draw.rect(screen, WHITE, (resolution[0]-150, 18, 131, 291), 2)
        pygame.draw.rect(screen, ORANGE, (resolution[0]-150, int(player.last_altitude/10)+18, 131, 76), 2)
        player.c_position = player.rect.center

    if player.rect.center[0] < 0:
        player.rect.center = (player.rect.center[0]+resolution[0], player.rect.center[1])
        player.c_position = player.rect.center
    elif player.rect.center[0] > resolution[0]:
        player.rect.center = (player.rect.center[0]-resolution[0], player.rect.center[1])
        player.c_position = player.rect.center
