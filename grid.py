import pygame
import math

#Constants
#colors
BLACK=(0,0,0)
GREEN=(0,150,0)
WHITE=(255,255,255)
GREY = (100,100,100)
LIGHT_GREY = (200,200,200)
YELLOW =(255,255,0)


SCREEN_WIDTH =900

SCREEN_HEIGHT =SCREEN_WIDTH/2

FPS=60

FOV = math.pi /3

HALF_FOV =FOV/2

CASTED_RAYS= 128 #Half the screen width

STEP_ANGLE = FOV/CASTED_RAYS

MAP_SIZE = 10

TILE_SIZE = int((SCREEN_WIDTH/2)/MAP_SIZE)

MAX_DEPTH = int(MAP_SIZE*TILE_SIZE)


#scale rays casted
SCALE = (SCREEN_WIDTH/2)/CASTED_RAYS


#grid
# grid_part =50

# grid_spacing = [x for x in range(grid_part, SCREEN_WIDTH, grid_part)]

# def grid(screen):
#     for i in grid_spacing:
#         pygame.draw.line(screen, GREEN, (i, 0), (i, SCREEN_WIDTH))
#         pygame.draw.line(screen, GREEN, (0, i), (SCREEN_WIDTH, i))


#img
guy= pygame.image.load("player.png")


#map 


MAP = (
    '##########'
    '#      ###'
    '#        #'
    '#        #'
    '#        #'
    '#     #  #'
    '#        #'
    '## ###   #'
    '##     ###'
    '##########'
)

def draw_map(screen):
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            square = row*MAP_SIZE +col
            pygame.draw.rect(
                screen,
                LIGHT_GREY if MAP[square]=='#' else GREY,
                (col*TILE_SIZE, row*TILE_SIZE,TILE_SIZE-2,TILE_SIZE-2)
            )



#classes 

class Player(pygame.sprite.Sprite):
    speed =5
    angle=0
    rotational_speed=math.radians(5)
    color_key =WHITE

    def __init__(self, image, x=SCREEN_WIDTH//4, y=SCREEN_HEIGHT//4):
        super().__init__()
        self.image= pygame.transform.scale(image,(15, 15))
        self.img1 = self.image
        self.image.set_colorkey(self.color_key)
        self.rect = image.get_rect()
        self.rect1 = self.rect
        self.rect.center = (x,y)

    def draw(self,screen):
        screen.blit(redi.img1, self.rect1)

    def move(self):
        #fix the movement per frame rate thing
        key = pygame.key.get_pressed()
        self.rotate()
        dx,dy=0,0

        if key[pygame.K_UP] or key[pygame.K_DOWN]:
            dx= int(self.speed*(math.sin(self.angle)))
            dy= int(self.speed*(math.cos(self.angle)))
            if key[pygame.K_DOWN]:
                dy*=-1
                dx*=-1
        if key[pygame.K_RIGHT]:
            self.angle += self.rotational_speed
            if self.angle <= 0:
                self.angle += 2*math.pi
                
        if key[pygame.K_LEFT]:
            self.angle -= self.rotational_speed
            if self.angle >= 2*math.pi:
                self.angle -= 2*math.pi

        #collision detection
        col =int((self.rect.centerx+dx)/TILE_SIZE)
        row =int((self.rect.centery+dy)/TILE_SIZE)
        square = row*MAP_SIZE +col
        if MAP[square] == '#':
            dx,dy=0,0
        self.rect.x += dx
        self.rect.y += dy

            

    def rotate(self):
        self.img1=pygame.transform.rotate(self.image,math.degrees(self.angle))
        self.rect1 = self.img1.get_rect()
        self.rect1.center = self.rect.center
        self.img1.set_colorkey(self.color_key)

        #update position

    def vision(self,screen):
        #left most angle of the FOV
        start_angle = self.angle-HALF_FOV
        # #direction
        # pygame.draw.line(screen, GREEN, self.rect.center,
        #                  (self.rect1.centerx + math.sin(self.angle)*40, 
        #                   self.rect1.centery + math.cos(self.angle)*40),3
        #                   )
        for ray in range(CASTED_RAYS):
            #cast ray 
            for depth in range(MAX_DEPTH):
                #ray coordinates
                target_x = self.rect1.centerx + math.sin(start_angle)*depth
                target_y = self.rect1.centery + math.cos(start_angle)*depth

                #Convert target x,y to map col,row
                col = int(target_x/TILE_SIZE)
                row = int(target_y/TILE_SIZE)

                square = row*MAP_SIZE + col


                if MAP[square] == "#":
                    pygame.draw.rect(screen, GREEN, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2))

                    pygame.draw.line(screen, YELLOW, self.rect.center,(target_x,target_y))
                    
                    #shade
                    color = 255/(1+depth*depth*0.0001)
                    COLOR = (color, color, color)
                    #fix fish eye 
                    depth*=math.cos(self.angle-start_angle)
                    #wall height
                    wall_height = 30000/(depth+0.0001)

                    if wall_height>SCREEN_HEIGHT:wall_height=SCREEN_HEIGHT-5

                    #draw 3D projection
                    pygame.draw.rect(screen,COLOR,(
                        SCREEN_HEIGHT+ray*SCALE,
                        (SCREEN_HEIGHT/2)-wall_height/2,
                        SCALE*3,wall_height))
                    break
                #floor prespective
                else:
                    floor_height = 1000000/(1+depth*depth+0.0001)
                    color = 255/(1+depth*depth*0.0001)
                    pygame.draw.rect(screen, (color,color,color),(
                        SCREEN_HEIGHT+ray*SCALE,
                        (SCREEN_HEIGHT/2)+floor_height/2,
                        SCALE*3, floor_height))
                    
            start_angle+=STEP_ANGLE

        
    

#instances
redi=Player(guy)


#floor and ground
def draw_3d(screen):
    pygame.draw.rect(screen, LIGHT_GREY, (SCREEN_WIDTH/2, 0,SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    pygame.draw.rect(screen,GREY,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,SCREEN_WIDTH/2,SCREEN_HEIGHT))

            
