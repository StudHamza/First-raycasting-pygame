from grid import *


pygame.init()
#setting window
background_colour = (BLACK)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Ray casting')


clock = pygame.time.Clock()

# Variable to keep our game loop running
running = True

#font
font=pygame.font.SysFont('Monospace Regular',30)


# game loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False
    screen.fill(background_colour)

    #3d Back ground 
    #draw_3d(screen)

    #redi
    draw_map(screen)
    redi.move()
    redi.draw(screen) 
    redi.vision(screen)

    #FPS
    fps=str(int(clock.get_fps()))
    fps_text = font.render(fps, False, (255, 255, 255))
    screen.blit(fps_text,(0,0))
    


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()