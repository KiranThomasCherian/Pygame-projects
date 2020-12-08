import  pygame
import os,sys
from grid_multi import Grid
import socket
import threading



pygame.init()
def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()




HOST='127.0.0.1'
PORT=9009
connection_established=False
conn,addr=None,None
 

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(1)

grid=Grid()
running=True
player="X"
turn=True
playing="True"


def wait_connect():
    global connection_established,conn,addr
    conn,addr=sock.accept()
    print('[client connected]')
    connection_established=True
    grid.game_over=False
    receive_data()

create_thread(wait_connect)
def receive_data():
    global turn,connection_established
    while True:
        try:
            data=conn.recv(1024).decode()
            data=data.split('-')
            x,y=int(data[0]),int(data[1])
            if data[2]=='Yourturn':
                turn=True
            if data[3] =="False":
                grid.game_over=True
            while playing!="True":
                pass        #busywait
            if grid.get_cell_value(x,y)==0:
                grid.set_cell_value(x,y,"O")
            #print(data)
            
        except:
            print('remote connection terminated')
            connection_established=False
            grid.clear_grid()
            grid.game_over=True
            create_thread(wait_connect)
            break


surface=pygame.display.set_mode((600,630))
pygame.display.set_caption('Tic-Tac-Toe :Server')



def status_bar():
    font = pygame.font.Font('assets/04b19.ttf', 16)
    if not connection_established:
        whoturn ="Not connected to opponent"
    elif grid.game_over:
        if grid.winner !=0:
            whoturn= " winner = " + player + " | press space to clear "
        else:
            whoturn="Game over | press space to clear"
        #print(whoturn)
    elif turn==True:
        whoturn="Your Turn" 
    else:
        whoturn="Opponent Turn"    
    text = font.render(f'Player X |  {whoturn}', True, (25,25,112),) 
    textRect = text.get_rect() 
    textRect.center = (300, 615)
    surface.blit(text, textRect)

while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running=False
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    #print(pos[0]//200,pos[1]//200)
                    cellx,celly=pos[0]//200,pos[1]//200
                    grid.set_mouse_input(cellx,celly,player)
                    if grid.game_over:
                        playing="False"
                    send_data='{}-{}-{}-{}'.format(cellx,celly,'Yourturn',playing).encode()
                    conn.send(send_data)
                    turn=False
                    # if grid.switch_player:
                    #     if player =="X":
                    #         player ="O"
                    #     else:
                    #         player="X"
                        #grid.print_grid()
                    if grid.game_over:
                        print("Game over")

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over=False
                playing="True"
                print("restart")
                if not connection_established:
                    grid.game_over=True

            elif event.key ==pygame.K_ESCAPE:
                running=False

    surface.fill((250,128,114))
    grid.draw(surface)
    status_bar()
    pygame.display.flip()