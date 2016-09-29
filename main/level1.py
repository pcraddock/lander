import functions
#I've split functions off into a different script for ease of editing/adding new levels/resolutions etc
import math
#math gives us access to absolute magnitude functions
import pygame
#pygame gives us easy graphics toys

def play(screen, clock, difficulty, muted, resource_location, resolution):
    #is the play function that's called by the launcher
    BLACK  = (  0,   0,   0)
    WHITE  = (255, 255, 255)
    GREEN  = (  0, 255,   0)
    YELLOW = (255, 255,   0)
    RED    = (255,   0,   0)
    ORANGE = (255, 127,   0)
    #the above is just defining RGB colours for text and screen changes

    def safe_landing(player_velocities, difficulty):
        #is a function that is called to determine whether a landing was safe or not
        if math.fabs(player_velocities[0]) <= difficulty and math.fabs(player_velocities[1]) <= difficulty:
            return True
        else:
            return False

    class Craft(pygame.sprite.Sprite):
        """Craft class for landers, child of Sprite"""
        def __init__(self):
            super(Craft, self).__init__()

            self.image = pygame.image.load(resource_location+"player_l.png").convert_alpha()
            #takes an image from the resources folder appropriate to the resolution to be used as the player
            self.rect = self.image.get_rect()
            #gets pygame to automatically work out the boundaries of the player
            self.mask = pygame.mask.from_surface(self.image)
            #gets pygame to build a mask that goes around the edge of the player for collision detection
            self.velocities = functions.resource("init_velocity", resolution)
            #variable stores the players velocity and is defaulted to an intial velocity value stored in the functions script
            self.c_position = functions.resource("init_position", resolution)
            #stores the players current position and is defaulted to a intial position value stored in the functions script
            self.angle = 0
            #stores the players angle and is defaulted to vertical
            self.thrust = 0
            #stores a value for the thrust currently exerted on the player, 0 unless the up button is being pressed
            self.angular_thrust = 0
            #stores a value for the angle change currently exerted on the player, 0 unless a sideways arrow key is pressed
            self.fuel = 100
            #stores a value for the amount of fuel that the player has
            self.fuel_rate = 0.2
            #defines the rate at which fuel is burnt for every frame in which the up arrow is pressed
            self.burn_sound = pygame.mixer.Sound("../resources/burn.ogg")
            #loads a burn sound to be played whilst thrusting
            self.explosion_sound = pygame.mixer.Sound("../resources/explosion.ogg")
            #loads an explosion sound to be played on crashing

        def update(self, accel_g):
            """ this is a function which is updated each frame to calculate where the player should next appear given their position, velocity, thrust, and the current gravity """
            if self.fuel <= 0.0:
                #checks to see if the fuel is empty (or less than empty since the fuel rate is simply subtracted from the total fuel)
                self.fuel = 0.0
                #sets the fuel level to 0 so that we don't see negetive amounts of fuel in the tank
                self.thrust = 0
                #stops the player from being able to thrust up if there's no fuel
            self.angle += self.angular_thrust
            #takes the players current angle and alters it by the angular thrust
            x_thrust = (self.thrust * math.sin(math.radians(float(self.angle))))
            #takes the thrust on the player and the players angle and works out the x component of that thrust
            y_thrust = (self.thrust * math.cos(math.radians(float(self.angle))))
            #takes the thrust on the player and the players angle and works out the y component of that thrust

            self.velocities = (self.velocities[0]+x_thrust, self.velocities[1]+accel_g-y_thrust)
            #changes the players velocity by adding gravity and thrust

            self.rect.center = (self.c_position[0]+int(round(self.velocities[0])), self.c_position[1]+int(round(self.velocities[1])))
            #moves the centre of the image for the player by adding on the velocity

            self.c_position = player.rect.center
            #sets the players current position to the centre of the image that describes it for the next pass

            if self.thrust == 0:
                #checks to see if the player is not thrusting
                self.image = pygame.image.load(resource_location+"player_l.png").convert_alpha()
                #ensures that the image describing the player is does not have flames coming out the bottom
            elif self.thrust != 0:
                #checks to see if the player is thrusting
                self.fuel -= self.fuel_rate
                #subtracts the amount of fuel previously set from the amount of fuel left
                self.image = pygame.image.load(resource_location+"player_ld.png").convert_alpha()
                #ensures that the image of the player has flames coming out of the bottom
            self.image = pygame.transform.rotate(self.image, -1*player.angle)
            #rotates the image of the player by its current angle

            return self.rect.center
            #returns the coordinates for the centre of the player

    class Planet(pygame.sprite.Sprite):
        """Object class for planet"""
        def __init__(self):
            super(Planet, self).__init__()

            self.name = "The Moon"
            #the name to be displayed in the top left info section
            self.image = pygame.image.load(resource_location+"moon_surface.png").convert_alpha()
            #the image used for the planet surface
            self.bg_image = resource_location+"moon.png"
            #the image used as a background for the planet (including planet surface)
            self.rect = self.image.get_rect()
            #calcultes the dimensions of the surface so that its location can be determined
            self.mask = pygame.mask.from_surface(self.image)
            #works out the border of the surface for collision detection
            self.accel_g = 0.1
            #the acceleration due to gravity from the planet
            self.rect.bottomleft = (0, resolution[1])
            #ensuring that the planet surface lines up with the bottom of the screen (which is resolution dependant unless we had huge images)
            self.thrust = 0.5
            #the thrust that the player can exert (don't ask me why I put this in this section...)

    sprite_list = pygame.sprite.Group()
    #creates a list of sprites
    planet = Planet()
    #make a planet called planet
    player = Craft()
    #make a craft called player
    sprite_list.add(player)
    #add the player to a list of sprites

    font_small = pygame.font.SysFont('Courier New', functions.resource("small_font", resolution), True, False)
    #define what font will be used to print the info in the top left depending on the resolution

    bg_img = pygame.image.load(planet.bg_image)
    #load the background image from the planet class onto the screen
    player.rect.center = player.c_position
    #load the image of the player onto the screen at its current position

    in_level = True
    #a variable to enable us to quit out of the level
    playing = True
    #a variable to check whether the game itself is running (so should leaking fuel still be being lost from the tank etc)
    safe_landing_check = True
    #check to see if we've landed safely
    next_level = False
    #check to see if we're advancing to the next level this frame

    if not muted:
        #check to see if we're muted (i know this looks weird, but it makes sense in other contexts)
        player.burn_sound = pygame.mixer.Sound("../resources/silence.ogg")
        #if we are muted then set the burn sound to silence
        player.explosion_sound = pygame.mixer.Sound("../resources/silence.ogg")
        #if we are muted then set the explosion sound to silence

    while in_level:
        #enables us to drop out of the level if we choose to
        while playing:
            #if the game is running
            for event in pygame.event.get():
                #check for input events to the game
                if event.type == pygame.QUIT:
                    #check to see if the x in the corner of the screen has been pressed
                    in_level = False
                    #if it has been then drop out to the main menu
                elif event.type == pygame.KEYDOWN:
                    #check to see if a key has been pressed
                    if event.key == pygame.K_UP and player.fuel > 0.0:
                        #check to see if the up arrow key was pressed and the player still has fuel
                        player.thrust = planet.thrust
                        #if so then give the player the predetermined amount of thrust
                        player.burn_sound.play()
                        #and play the rocket sound
                    elif event.key == pygame.K_LEFT:
                        #check to see if the left arrow key was pressed
                        player.angular_thrust = -2
                        #if it was then produce angular thrust of -2
                    elif event.key == pygame.K_RIGHT:
                        #check to see if the right arrow key was pressed
                        player.angular_thrust = 2
                        #if it was then produce angular thrust of 2
                    elif event.key == pygame.K_ESCAPE:
                        #check to see if the esc key was pressed
                        in_level = False
                        #if it was then drop back to the main menu
                elif event.type == pygame.KEYUP:
                    #check to see if a key has been released
                    if event.key == pygame.K_UP:
                        #if the up arrow key has been released
                        player.thrust = 0
                        #then stop the player from thrusting
                        player.burn_sound.stop()
                        #and stop the burn sound
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        #if either of the direction arrows was released
                        player.angular_thrust = 0
                        #stop the players angle from altering further
                        #we could potentially remove this if we wanted scientific accuracy, but it makes the game seriously fucking difficult

            screen.fill(BLACK)
            #wipe anything from the screen
            screen.blit(bg_img, [0,0])
            #display the background image on the screen

            player.rect.center = player.update(planet.accel_g)
            #update the center of the player based on the update function defined in the craft definition at the top

            planet_tag = font_small.render("Planet: "+str(planet.name), True, WHITE)
            #create the text that names the planet
            if math.fabs(player.velocities[0]) > difficulty:
                #check to see if the horizontal velocity is above the difficulty level (of max landing velocity)
                x_vel_txt = font_small.render("Horizontal velocity: "+str(round(player.velocities[0], 1)), True, RED)
                #if it is then create the text that shows horizontal velocity in red
            else:
                x_vel_txt = font_small.render("Horizontal velocity: "+str(round(player.velocities[0], 1)), True, GREEN)
                #if its not then create the text that shows the horizontal velocity in green
            if math.fabs(player.velocities[1]) > difficulty:
                #check to see if the vertical velocity is above the difficulty level (of max landing velocity)
                y_vel_txt = font_small.render("Vertical velocity: "+str(round(player.velocities[1], 1)), True, RED)
                #if it is then create the text that shows vertical velocity in red
            else:
                y_vel_txt = font_small.render("Vertical velocity: "+str(round(player.velocities[1], 1)), True, GREEN)
                #if its not then create the text that shows horizontal velocity in green

            if player.fuel > 75:
                #check to see if the fuel is more than 75 percent full
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, GREEN)
                #if it is then create the fuel text in green
            elif player.fuel > 50:
                #check to see if its more than 50 percent full (but less than 75)
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, YELLOW)
                #if it is then create the fuel text in yellow
            elif player.fuel > 25:
                #check to see if its more than 25 percent full (but less than 50)
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, ORANGE)
                #if it is then create the fuel text in orange
            elif player.fuel > 0:
                #check to see if the fuel level is between 0 and 25 percent full
                fuel_txt = font_small.render("Fuel: "+str(round(math.fabs(player.fuel), 1))+"% [FUEL LOW]", True, RED)
                #if it is then create the fuel text in red
            elif player.fuel == 0:
                #check to see if there's no fuel left
                fuel_txt = font_small.render("Fuel: 0% [FUEL EMPTY]", True, RED)
                #if there's not then display that in red

            screen.blit(x_vel_txt, functions.resource("x_vel_txt", resolution))
            #display the horizontal velocity text on the screen (in a place appropraite for the resolution)
            screen.blit(y_vel_txt, functions.resource("y_vel_txt", resolution))
            #display the vertical velocity text on the screen (in a place appropraite for the resolution)
            screen.blit(fuel_txt, functions.resource("fuel_txt", resolution))
            #display the fuel level on the screen (in a place appropraite for the resolution)
            screen.blit(planet_tag, functions.resource("planet_tag", resolution))
            #display the planet name on the screen (in a place appropraite for the resolution)

            if pygame.sprite.collide_mask(player, planet) != None:
                #check to see if the player has collide with the planet
                player.burn_sound.stop()
                #if it has then stop the engine burning sound
                player, safe_landing_check, playing = functions.surface_collision(screen, resolution, player, difficulty)
                #call the safe landing check function described above, and remember whether the landing was safe or not

            if player.rect.center[0] < 0:
                #check to see if the player is more than half off the left hand side of the screen
                player.rect.center = (player.rect.center[0]+resolution[0], player.rect.center[1])
                #if it is then put the player on the right hand side of the screen
                player.c_position = player.rect.center
                #and update the players position so that calculations work in the next pass
            elif player.rect.center[0] > resolution[0]:
                #check to see if the player is more than half off the right hand side of the screen (depends on the resolution)
                player.rect.center = (player.rect.center[0]-resolution[0], player.rect.center[1])
                #if it is then put the player on the left hand side of the screen
                player.c_position = player.rect.center
                #and update its position
            elif player.rect.center[1] < 0:
                #check to see if the player is falling off the top of the screen
                player.rect.center = (player.rect.center[0], 0)
                #if it is then stop it moving further up
                player.c_position = player.rect.center
                #and remember this for the next pass

            sprite_list.draw(screen)
            #display the player on the screen
            clock.tick(30)
            #ensure that at least 1/30th of a second has passed

            frame_rate = clock.get_fps()
            #gets the current framerate of the game
            frame_rate_txt = font_small.render("FPS: "+str(round(frame_rate, 1)), True, WHITE)
            #generates text to render that frame rate
            screen.blit(frame_rate_txt, functions.resource("frame_rate_txt", resolution))
            #prints that text on the screen in an appropriate place for the chosen resolution

            pygame.display.flip()
            #show the screen to the user

        for event in pygame.event.get():
            #if we're no longer playing i.e. on a crash or success screen check for events
            if event.type == pygame.QUIT:
                #check for clicking on the x in the corner of the window
                in_level = False
                #close the level if its clicked
            elif event.type == pygame.KEYDOWN:
                #check for the pushing down of a key
                if event.key == pygame.K_a:
                    #check for the a key being pressed, which replays the level
                    player.c_position = functions.resource("init_position", resolution)
                    #reset the player position
                    player.velocities = functions.resource("init_velocity", resolution)
                    #reset the player velocity
                    player.angle = 0
                    #reset the player tilt
                    player.angular_thrust = 0
                    #reset the player thrust
                    player.fuel = 100
                    #reset the player fuel
                    playing = True
                    #get back into the playing loop
                if event.key == pygame.K_SPACE:
                    #check for the space key being pressed
                    player.c_position = functions.resource("init_position", resolution)
                    #reset the player position
                    player.velocities = functions.resource("init_velocity", resolution)
                    #reset the player velocity
                    player.angle = 0
                    #reset the player angle
                    player.angular_thrust = 0
                    #reset the player thrust
                    player.fuel = 100
                    #reset the player fuel
                    if safe_landing_check == True:
                        #check if the landing was safe
                        next_level = True
                        #if it was then tell launcher.py to try the next level
                        in_level = False
                        #and break out of this level
                    elif safe_landing_check == False:
                        playing = True
                        #if the landing wasn't safe replay the current level
                if event.key == pygame.K_ESCAPE:
                    #check if esc key is pressed
                    in_level = False
                    #if it is break out to the launcher screen

#this bit returns true or false depending on whether you've chosen to go to the next level or not, for processing by launcher.py
    if next_level == False:
        return False
    elif next_level == True:
        return True
