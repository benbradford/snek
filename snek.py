import pygame
from pygame.locals import *
import random

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def tuple(self):
        return (self.x, self.y)

    def has_collided_with(self, other):
        return self.x == other.x and self.y == other.y

pygame.init()

# Constants
SCREEN_SIZE = Vec(600, 600)
CELL_SIZE = 20
SPEED = 11


window = pygame.display.set_mode(SCREEN_SIZE.tuple())
pygame.display.set_caption("SNEK GAME")
clock = pygame.time.Clock()

def get_random_position():
    return Vec (random.randrange(CELL_SIZE,SCREEN_SIZE.x -CELL_SIZE,CELL_SIZE),random.randrange(CELL_SIZE*2,SCREEN_SIZE.y-CELL_SIZE,CELL_SIZE))

time=0
score=0 
body=[Vec(200,200), Vec(200,200-CELL_SIZE), Vec(200,200-(CELL_SIZE*2)), Vec(200-CELL_SIZE,200-(CELL_SIZE*2))]
dir=Vec(0,CELL_SIZE)
apple=get_random_position()
bad_apple = get_random_position()
is_running = True
is_quit = False

def is_valid_position(pos):
    for b in body:
        if b.has_collided_with(pos):
            return False
    return True

def get_valid_random_position():

    pos = get_random_position()
    while not is_valid_position(pos):
        pos = get_random_position()
    return pos

def render():
    window.fill((255,245,110))
    for b in range(0,len(body)-1):
        pygame.draw.rect(window,(40,150,50),(body[b].x,body[b].y,CELL_SIZE,CELL_SIZE))
        
    pygame.draw.circle(window,(225,125,0),(bad_apple.x+(CELL_SIZE/2),bad_apple.y+(CELL_SIZE/2)),CELL_SIZE/2)
    pygame.draw.circle(window,(240,0,0),(apple.x+(CELL_SIZE/2),apple.y+(CELL_SIZE/2)),CELL_SIZE/2)
    
    pygame.draw.line(window,(100,100,200),(0,36),(SCREEN_SIZE.x,36),7)
    pygame.draw.line(window,(100,100,200),(0,30),(0,SCREEN_SIZE.y),12)
    pygame.draw.line(window,(100,100,200),(SCREEN_SIZE.x,30),(SCREEN_SIZE.x,SCREEN_SIZE.y),12)
    pygame.draw.line(window,(100,100,200),(0,SCREEN_SIZE.y),(SCREEN_SIZE.x,SCREEN_SIZE.y),12)
    
    font = pygame.font.SysFont("handwriting", 26)
    text_surface = font.render("Score " + str(score), True, (40,150,50)) 
    window.blit(text_surface, (CELL_SIZE,7))
    
    text_surface = font.render("Time " + str(time),True, (40,150,50))
    window.blit(text_surface,  (SCREEN_SIZE.x-100,7))
    

    if not is_running:
        font = pygame.font.SysFont("algerian", 46)
        text_surface = font.render("Press Space to Quit " ,True, (40,150,50))
        window.blit(text_surface,  (SCREEN_SIZE.x / 4, SCREEN_SIZE.y / 2))
    
    pygame.display.flip()


while is_running:
    clock.tick(SPEED)
    time = time+ (1.0 / SPEED)
    
    # events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if (event.key == K_w or event.key == K_UP) and dir.y!=CELL_SIZE: 
                dir = Vec(0,-CELL_SIZE)
                break
            elif (event.key == K_s or event.key == K_DOWN) and dir.y!=-CELL_SIZE: 
                dir = Vec(0,CELL_SIZE)
                break
            elif (event.key == K_a or event.key == K_LEFT) and dir.x!=CELL_SIZE: 
                dir = Vec(-CELL_SIZE,0)
                break
            elif (event.key == K_d or event.key == K_RIGHT) and dir.x!=-CELL_SIZE: 
                dir = Vec(CELL_SIZE,0)
                break

     
    render()

    # logic     
    for b in range (len (body)-1,0,-1):
        # see if we have eaten ourselves
        if b != 0:
            if body[b].has_collided_with(body[0]):
                is_running = False
        # move body along 1 in the array
        body[b].x=body[b-1].x
        body[b].y=body[b-1].y

    # see if we have exited the screen
    if body[0].x < 0 or body[0].x >= SCREEN_SIZE.x or body[0].y >= SCREEN_SIZE.y or body[0].y <= CELL_SIZE or body[0].x == bad_apple.x and body[0].y == bad_apple.y:
        is_running = False

    # update the head to the new position based on the current direction
    body[0].x=body[0].x+dir.x
    body[0].y=body[0].y+dir.y

    # see if we have eaten an apple
    if body[0].has_collided_with(apple):
        i=len(body)-1
        score=score+1
        body.append(Vec(body[i].x,body[i].y))
        apple=get_valid_random_position()
        bad_apple=get_valid_random_position()
        while bad_apple.has_collided_with(apple):
            bad_apple=get_valid_random_position()

    # see if we have eaten a bad apple
    if body[0].has_collided_with(bad_apple):
        is_running = False


while not is_quit:
    clock.tick(60)
    render()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_quit = True

pygame.quit()
