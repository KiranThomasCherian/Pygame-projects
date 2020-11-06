import pygame
import sys
import random

pygame.init()

screen =pygame.display.set_mode((576,830))
bg_surface=pygame.image.load("assets/background-day.png").convert()
bg_surface=pygame.transform.scale2x(bg_surface)
floor_surface =pygame.image.load("assets/base.png").convert()
floor_surface =pygame.transform.scale2x(floor_surface)
clock =pygame.time.Clock()
gfont=pygame.font.Font("assets/04b19.ttf",40)


floor_x_pos=0
gravity =0.2
bird_movement =0
game_active=True
score=0
highscore=0

def show_score(cur_state):

    score_surface=gfont.render(f'Score :{int(score)}',True,(255,255,255))
    score_rect=score_surface.get_rect(center=(288,100))
    screen.blit(score_surface,score_rect)
    if cur_state == "gameover":
        hscore_surface=gfont.render(f'High Score :{int(highscore)}',True,(255,255,255))
        hscore_rect=hscore_surface.get_rect(center=(288,200))
        screen.blit(hscore_surface,hscore_rect)

#gameover_surface=pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
gameover_surface=pygame.image.load("assets/message.png").convert_alpha()
gameover_rect=gameover_surface.get_rect(center=(288,430))
def drawfloor() :
    global floor_x_pos
    screen.blit(floor_surface,(floor_x_pos,750))
    screen.blit(floor_surface,(floor_x_pos+576,750))

    if floor_x_pos < -576:
        floor_x_pos=0

bird_surface =pygame.image.load("assets/redbird-midflap.png").convert()
bird_surface =pygame.transform.scale2x(bird_surface)
bird_rect=bird_surface.get_rect(center =(100,430))

pipe_surface =pygame.image.load("assets/pipe-green.png").convert()
pipe_surface =pygame.transform.scale2x(pipe_surface)
pipe_list=[]
pipe_height=[600,400,500,200]

SPAWNPIPE =pygame.USEREVENT   # caps by convevtion
pygame.time.set_timer(SPAWNPIPE,1200)

def create_pipe():
    pheight=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop =(700,pheight))
    top_pipe=pipe_surface.get_rect(midbottom =(700-20,pheight-260))
    return bottom_pipe,top_pipe

def move_pipe(pipes):  
    for pipe in pipes:
        pipe.centerx -=5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=840:
            screen.blit(pipe_surface,pipe)
        else:
            fliped = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(fliped,pipe)

def check_col(pipes):
    for pipe in pipes :
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <=-150 or bird_rect.bottom >750 :
        return False
    return True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if event.key ==pygame.K_SPACE and game_active==True:
                bird_movement=0
                bird_movement-=8   
            if event.key ==pygame.K_SPACE and game_active==False:
                pipe_list.clear()
                bird_rect.center=(100,430)
                bird_movement=0
                game_active=True
                score =0

        if event.type ==SPAWNPIPE:
            pipe_list.extend(create_pipe())
            #print(len(pipe_list))
            if(len(pipe_list)>16):
                pipe_list.clear()





    screen.blit(bg_surface,(0,-100)) 
    
    bird_movement+=gravity
    if game_active: 
        screen.blit(bird_surface,bird_rect)
        bird_rect.centery+=bird_movement 
        game_active=check_col(pipe_list)
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score+=0.1
        show_score('game')
    else:
        if score > highscore:
            highscore=score
        show_score('gameover')
        screen.blit(gameover_surface,gameover_rect)
    floor_x_pos-=1
    drawfloor()


    pygame.display.update()
    clock.tick(90)