import pygame

def play(screen, clock, resolution, resource_location):
    pygame.mixer.quit()
    playing=True
    return True 
"""    video = pygame.movie.Movie("..\resources\1280x720\video1.mpg")
    video.set_display(screen)
    video.play()
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.stop()
                playing = False
            elif event.type == pygame.KEYDOWN:
                video.stop()
                playing =  False
        screen.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(30)
        playing = video.get_busy()
    return True
"""