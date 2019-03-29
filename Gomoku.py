import pygame,sys,numpy as np
from pygame import *
def extend(x,y):
    # x,y 是由从(x,y)坐标来开始向 上(下),右上(左下),右(左),右下(左上)进行遍历
    tx,ty = x,y
    dx = [0,1,1,1]
    dy = [-1,-1,0,1]
    count = [1]*4;
    for f in (1, -1):
        for m in range(4):
            while data[ty,tx] != 0 and 0<= tx < len_x and  0<= ty < len_y:
                tx, ty = tx + dx[m] * f, ty + dy[m] * f
                if data[ty,tx] % 2 != data[y,x]:#判断是不是相同颜色的子
                    break                       #这个方向直接放弃
                count[m] = count[m] + 1

    if max(count) >= 5:
        # print(data)
        return data[y,x]
    else:
        return 0
def find_winner():
    global len_x,len_y,data
    for i in range(len_x):
        for j in range(len_y):
            if data[j,i] == 0:
                continue
            ex = extend(i,j)
            if ex == 0:
                continue
            fontcolor = [(255,255,255),(0,0,0)]
            textSurface = textFont.render(who_down[ex % 2] + " is winner!", True, fontcolor[ex % 2])
            textrect = textSurface.get_rect()
            screen.blit(textSurface, ((width-textrect.width)//2,0))
            return True
    return False
def alpha_beta(data):
    """

    棋盘的下子情况
    数据的表示使用0:未下棋子,奇数:先下的棋子,双数:后下的棋子.
    :param data:
    返回机器根据现有的棋盘下子的情况,给出下一次下子的位置 :return:
    """
    return x,y
    pass
def down_board(xy,B_A):
    x,y = xy
    dx,dy = x-sx,y-sy
    ix,iy = 0,0
    while dx >= L//2:
        ix = ix + 1
        dx = dx - L
    while dy >= L//2:
        iy = iy + 1
        dy = dy - L
    tx = x + (-dx) if dx < L//2 else (L-dx)
    ty = y + (-dy) if dy < L//2 else (L-dy)
    # print(tx,ty)
    qizi = pygame.image.load("./image/black.png")
    if B_A == "WHITE":
        qizi = pygame.image.load("./image/white.png")
    rect = pygame.Rect(tx - R,ty - R, 2*R, 2*R)
    if data[iy][ix] == 0 and x >= sx-R and x <= width - R and y >= sy-R and y <= height - R:
        global index
        index = index + 1
        data[iy][ix] = index
        screen.blit(qizi,rect)
        # 每下完一次棋子之后都需要进行判断一次是不是有赢家.
        have_winner = find_winner()
        return have_winner

def restart_game():
    global data,index
    data = [[0] * len_x for i in range(len_y)]
    data = np.array(data)
    index = 0
    screen.blit(board, boardrect)

    pass
def main():
    while True:
        #for 循环这个判断获取事件的内容必须要写在while中的开头
        for event in pygame.event.get():
            #这个地方不是什么时候都会更新的,只有在有时间发生变化的时候这个地方才会执行,或者判断
            #一般是在敲击键盘的时候,或者光标在窗体内移动的时候回有更新,刷新.
            if event.type == pygame.QUIT:
                print(data)
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                xy = list(pygame.mouse.get_pos())
                global is_start
                if not is_start and showRect.collidepoint(xy[0],xy[1]):
                    screen.blit(board, boardrect)
                    is_start = True
                    break
                if pressed_array[0] == 1:
                    if down_board(xy,"BLACK"):
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                elif pressed_array[2] == 1:
                    if down_board(xy,"WHITE"):
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            elif event.type == pygame.KEYDOWN:
                k_down = pygame.key.get_pressed()
                if k_down[pygame.K_SPACE] == 1:
                    print("Restart")
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                    restart_game()

        pygame.display.update()

        fclock.tick(fps)
    pass
is_start = False
who_down = ["White","Black"]
len_x,len_y = 15,15
data = [[0]*len_x for i in range(len_y)]
data = np.array(data)
index = 0
size = width,height = 535, 535
sx,sy = 22,22
L = 35
speed = [1,1]
BLACK = 0,0,0
WHITE = 255,255,255
fps = 30
fclock = pygame.time.Clock()
R = 14 #棋子的半径
pygame.init()
# 初始化窗口,执行玩这个地方的代码就回直接生成一个新的窗口
# screen 是一个类,set_mode是用来初始化一个窗口的,并且size是初始化窗口的大小的.mode:模型
screen = pygame.display.set_mode(size)
#caption : 标题
pygame.display.set_caption("Gomoku")
#窗口的显示和设置大小都是在display中的
#board没有move函数,但是boardrect是有move函数的.
board = pygame.image.load("./image/board.jpg")
white = pygame.image.load("./image/white.png")
boardrect=board.get_rect()
start = pygame.image.load("./image/start.png")
startrect=start.get_rect()
showRect = pygame.Rect(width//2-startrect.width//2,height//2-startrect.height//2,startrect.width, \
                       startrect.height)
textFont = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuibold", 30)
screen.blit(start,showRect)
# screen.blit(board,boardrect)
main()


