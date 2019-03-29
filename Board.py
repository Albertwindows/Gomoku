import pygame, sys, numpy as np
from pygame import *
from pygame import gfxdraw
from alpha_beta import *


class Board(object):
    pre_pos = [-1,-1]
    who_first = 1                       #1:用户先下     2:电脑先下
    is_start = False                    #开始的标志位
    game_over = False
    who_down = ["WHITE", "BLACK"]
    len_x, len_y = 15, 15               #棋盘横纵的格子数
    index = 1                           #棋子的编号:初始化就是1,从1开始
    title = "Gomoku"
    sx, sy = 22, 22
    L = 35
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    fps = 30
    fclock = pygame.time.Clock()
    R = 14                              # 棋子的半径

    def __init__(self, width, height):
        self.board = pygame.image.load("./image/board.jpg")
        self.board_rect = self.board.get_rect()
        self.data = [[0] * self.len_x for i in range(self.len_y)]
        self.data = np.array(self.data)
        self.size = self.height, self.width = width, height
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.start = pygame.image.load("./image/start.png")
        self.start_rect = self.start.get_rect()
        self.showRect = pygame.Rect(self.width // 2 - self.start_rect.width // 2,
                                    self.height // 2 - self.start_rect.height // 2,
                                    self.start_rect.width,
                                    self.start_rect.height)
        self.textFont = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuibold", 30)
        self.screen.blit(self.start, self.showRect)
        self.main()

    def extend(self, x, y):
        # x,y 是由从(x,y)坐标来开始向 上(下),右上(左下),右(左),右下(左上)进行遍历
        tx, ty = x, y
        dx = [0, 1, 1, 1]
        dy = [-1, -1, 0, 1]
        count = [1] * 4
        for f in (1, -1):
            for m in range(4):
                tx, ty = tx + dx[m] * f, ty + dy[m] * f
                while 0 <= tx < self.len_x and 0 <= ty < self.len_y and self.data[ty, tx] != 0:

                    if self.data[ty, tx] % 2 != self.data[y, x] % 2:  # 判断是不是相同颜色的子
                        break  # 这个方向直接放弃
                    count[m] = count[m] + 1
                    tx, ty = tx + dx[m] * f, ty + dy[m] * f
                #换方向的时候需要更新tx,ty的值
                tx, ty = x, y
        if max(count) >= 5:
            return self.data[y, x]
        else:
            return 0

    def find_winner(self,x,y):
        ex = self.extend(x, y)
        if ex == 0:
            return False
        font_color = [(255, 255, 255), (0, 0, 0)]
        text_surface = self.textFont.render(self.who_down[ex % 2] + " is winner!", True, font_color[ex % 2])
        text_rect = text_surface.get_rect()
        self.screen.blit(text_surface, ((width - text_rect.width) // 2, 0))
        return True

    def alpha_beta(self):
        """

        棋盘的下子情况
        数据的表示使用0:未下棋子,奇数:先下的棋子,双数:后下的棋子.
        :param data:
        返回机器根据现有的棋盘下子的情况,给出下一次下子的位置 :return:
        """
        data = self.data.copy()
        al = alpha_beta(data,self.index,self.pre_pos)
        pos = al.run()
        # print("score = {},(x,y) = ({})".format(score,pos))
        return pos

    def get_pos(self, x,y , mark=1):
        # mark = 1: x,y 是鼠标点击的位置(不一定是精确的位置) return-> 棋盘位置
        # mark = 0: x,y 是棋盘的位置,return-> 棋盘精确的位置
        # x,y = xy[0],xy[1]
        if mark == 0:
            return self.sx + self.L * x, self.sy + self.L * y

        dx, dy = x - self.sx, y - self.sy
        L = self.L
        ix = int(np.floor(dx/L-0.5)) + 1
        iy = int(np.floor(dy/L-0.5)) + 1
        tx,ty = int(self.sx + self.L * ix), int(self.sy + self.L *iy)
        print("ix={},iy={}".format(ix,iy))
        return ix, iy, tx, ty

    # xy 是鼠标点击的位置或者电脑给出的位置
    # B_A下什么子: "WHITE"白色的子,"BLACK"黑色的子
    def down_board(self, x, y, B_A="BLACK"):
        my_color = {"BLACK":(0,0,0),"WHITE":(255,255,255)}
        (ix, iy, tx, ty) = self.get_pos(x,y)
        R, sx, sy, width, height= self.R, self.sx, self.sy,self.width,self.height
        if self.data[iy, ix] == 0 and sx - R <= x <= width - R and sy - R <= y <= height - R:

            self.data[iy,ix] = self.index
            self.index = self.index + 1

            gfxdraw.aacircle(self.screen,tx,ty,R,my_color[B_A])
            gfxdraw.filled_circle(self.screen,tx,ty,R,my_color[B_A])
            pygame.display.update()
            have_winner = self.find_winner(ix,iy) #把现在下的子的位置传过去,就可以判断谁赢
            return have_winner
        return None

    def restart_game(self):
        self.data = [[0] * self.len_x for i in range(self.len_y)]
        self.data = np.array(self.data)
        self.index = 1
        self.screen.blit(self.board, self.board_rect)
    def pos_is_right(self,x_pos,y_pos):
        dl = self.L / 2
        flag = self.sx - dl <= x_pos < self.width - dl and self.sy -dl <= y_pos < self.height
        return flag
    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.data)
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos,y_pos = list(pygame.mouse.get_pos())
                    if not self.pos_is_right(x_pos,y_pos):
                        # print(x_pos,y_pos)
                        # print(self.get_pos(x_pos,y_pos))
                        break
                    if not self.is_start:
                        if not self.showRect.collidepoint(x_pos,y_pos):
                            continue
                        self.screen.blit(self.board, self.board_rect)
                        self.is_start = True
                        #下面是测试代码,实现电脑先下的功能
                        if self.who_first == 0:
                            # 如果电脑先下,默认先下(7,7)的位置
                            x_ai, y_ai = self.get_pos(7, 7, mark=0)
                            self.down_board(x_ai, y_ai, "BLACK")
                            self.is_start = True
                            break
                    else:#已经开始了,就开始下棋
                        ix,iy,tx,ty = self.get_pos(x_pos,y_pos)
                        if self.data[iy,ix] != 0:
                            break
                        # a = self.who_first
                        # b = self.index % 2 #标志当前改谁下了 奇数:黑子,偶数:白子
                        #
                        chess_color = self.who_down
                        # next_down = (not a and not b) or (a and b)

                        #什么时候都是先用户下,再电脑下
                        if not self.game_over:
                            if self.down_board(x_pos, y_pos, chess_color[self.index % 2]):
                                self.game_over = True
                            self.pre_pos = [ix,iy]
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)



                        if not self.game_over:
                            pos = self.alpha_beta()
                            [ix,iy] = pos
                            print("cpu:({}{})".format(ix,iy))
                            x_ai, y_ai = self.get_pos(ix, iy, mark=0)

                            if self.down_board(x_ai, y_ai, chess_color[self.index % 2]):
                                self.game_over = True
                            print("更改了" if self.data[iy,ix] else "没有更改")
                        if not self.game_over:
                            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                elif event.type == pygame.KEYDOWN:
                    k_down = pygame.key.get_pressed()
                    if k_down[pygame.K_SPACE] == 1:
                        print("Restart")
                        self.game_over = False
                        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                        self.restart_game()

            pygame.display.update()

            self.fclock.tick(self.fps)
        pass
if __name__ == "__main__":
    size = width, height = 535, 535
    aBoard = Board(width, height)

