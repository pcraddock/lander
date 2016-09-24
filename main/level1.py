import pygame, math, functions

def play(screen, clock, difficulty, muted, resource_location, resolution):
    BLACK  = (  0,   0,   0)
    WHITE  = (255, 255, 255)
    GREEN  = (  0, 255,   0)
    YELLOW = (255, 255,   0)
    RED    = (255,   0,   0)
    ORANGE = (255, 127,   0)

    def safe_landing(player_velocities, difficulty):
        if math.fabs(player_velocities[0]) <= difficulty and math.fabs(player_velocities[1]) <= difficulty:
            return True
        else:
            return False

    class Craft(pygame.sprite.Sprite):
        """Craft class for landers, child of Sprite"""
        def __init__(self):
            super(Craft, self).__init__()

            self.image = pygame.image.load(resource_location+"player_l.png").convert_alpha()
            #self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.velocities = [20, 0]
            self.c_position = [105, 75]
            self.angle = 0
            self.thrust = 0 #N
            self.angular_thrust = 0 #degrees
            self.fuel = 100 #percent
            self.fuel_rate = 0.2 #percent per thrust
            self.burn_sound = pygame.mixer.Sound("../resources/burn.ogg")
            self.explosion_sound = pygame.mixer.Sound("../resources/explosion.ogg")

        def update(self, accel_g):
            #determine componenet thrusts by angle
            if self.fuel <= 0.0:
                self.fuel = 0.0
                self.thrust = 0
            self.angle += self.angular_thrust
            x_thrust = int(round(self.thrust * math.sin(math.radians(float(self.angle)))))
            y_thrust = int(round(self.thrust * math.cos(math.radians(float(self.angle)))))

            #change velocity by adding gravity and thrust
            self.velocities = (self.velocities[0]+x_thrust, self.velocities[1]+accel_g-y_thrust)

            #displace player by velocity
            self.rect.center = (self.c_position[0]+self.velocities[0], self.c_position[1]+self.velocities[1])

            #update player position
            self.c_position = player.rect.center

            #make the change graphically
            if self.thrust == 0:
                self.image = pygame.image.load(resource_location+"player_l.png").convert_alpha()
            elif self.thrust != 0:
                #reduce fuel amount
                self.fuel -= self.fuel_rate
                self.image = pygame.image.load(resource_location+"player_ld.png").convert_alpha()
            self.image = pygame.transform.rotate(self.image, -1*player.angle)

            return self.rect.center

    class Planet(pygame.sprite.Sprite):
        """Object class for planet"""
        def __init__(self):
            super(Planet, self).__init__()

            self.name = "The Moon"
            self.image = pygame.image.load(resource_location+"moon_surface.png").convert_alpha()
            self.bg_image = resource_location+"moon.png"
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.accel_g = int(round(1.62)) #m/s
            self.rect.bottomleft = (0, 1080)
            self.thrust = 3

    #Create a list of sprites
    sprite_list = pygame.sprite.Group()
    planet = Planet()
    player = Craft()
    sprite_list.add(player)

    #text stuff
    font_small = pygame.font.SysFont('Courier New', 30, True, False)

    bg_img = pygame.image.load(planet.bg_image)
    player.rect.center = player.c_position

    in_level = True
    playing = True
    safe_landing_check = True
    next_level = False

    if not muted:
        player.burn_sound = pygame.mixer.Sound("../resources/silence.ogg")
        player.explosion_sound = pygame.mixer.Sound("../resources/silence.ogg")

    while in_level:
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_level = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and player.fuel > 0.0:
                        player.thrust = planet.thrust
                        player.burn_sound.play()
                    elif event.key == pygame.K_LEFT:
                        player.angular_thrust = -2
                    elif event.key == pygame.K_RIGHT:
                        player.angular_thrust = 2
                    elif event.key == pygame.K_ESCAPE:
                        in_level = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player.thrust = 0
                        player.burn_sound.stop()
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.angular_thrust = 0

            #Clear screen and apply background image
            screen.fill(BLACK)
            screen.blit(bg_img, [0,0])

            #Move player craft due to gravity and thrusting
            player.rect.center = player.update(planet.accel_g)

            #Display stats on screen in appropriate colour
            planet_tag = font_small.render("Planet: "+str(planet.name), True, WHITE)
            if math.fabs(player.velocities[0]) > difficulty:
                x_vel_txt = font_small.render("Horizontal velocity: "+str(player.velocities[0]), True, RED)
            else:
                x_vel_txt = font_small.render("Horizontal velocity: "+str(player.velocities[0]), True, GREEN)
            if math.fabs(player.velocities[1]) > difficulty:
                y_vel_txt = font_small.render("Vertical velocity: "+str(player.velocities[1]), True, RED)
            else:
                y_vel_txt = font_small.render("Vertical velocity: "+str(player.velocities[1]), True, GREEN)

            #Display fuel level on screen in appropriate colour
            if player.fuel > 75:
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, GREEN)
            elif player.fuel > 50:
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, YELLOW)
            elif player.fuel > 25:
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, ORANGE)
            elif player.fuel > 0:
                fuel_txt = font_small.render("Fuel: "+str(round(math.fabs(player.fuel), 1))+"% [FUEL LOW]", True, RED)
            elif player.fuel == 0:
                fuel_txt = font_small.render("Fuel: 0% [FUEL EMPTY]", True, RED)

            screen.blit(x_vel_txt, [15, 15])
            screen.blit(y_vel_txt, [15, 45])
            screen.blit(fuel_txt, [15, 75])
            screen.blit(planet_tag, [15, 105])

            #Check for landing/collision with surface
            if pygame.sprite.collide_mask(player, planet) != None:
                player.burn_sound.stop()
                player, safe_landing_check, playing = functions.surface_collision(screen, resolution, player, difficulty)

            #Check for falling off screen
            if player.rect.center[0] < 0:
                #If falling off left, move onto right
                player.rect.center = (player.rect.center[0]+1920, player.rect.center[1])
                player.c_position = player.rect.center
            elif player.rect.center[0] > 1920:
                #If falling off right, move onto left
                player.rect.center = (player.rect.center[0]-1920, player.rect.center[1])
                player.c_position = player.rect.center
            elif player.rect.center[1] < 0:
                #If falling off top, prevent further upward movement
                player.rect.center = (player.rect.center[0], 0)
                player.c_position = player.rect.center

            #Draw sprites
            sprite_list.draw(screen)
            clock.tick(25)
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_level = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.c_position = [105, 75]
                    player.velocities = [20, 0]
                    player.angle = 0
                    player.angular_thrust = 0
                    player.fuel = 100
                    playing = True
                if event.key == pygame.K_SPACE:
                    player.c_position = [105, 75]
                    player.velocities = [20, 0]
                    player.angle = 0
                    player.angular_thrust = 0
                    player.fuel = 100
                    if safe_landing_check == True:
                        next_level = True
                        in_level = False
                    elif safe_landing_check == False:
                        playing = True
                if event.key == pygame.K_ESCAPE:
                    in_level = False

    if next_level == False:
        return False
    elif next_level == True:
        return True
