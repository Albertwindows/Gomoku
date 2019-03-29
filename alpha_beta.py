import numpy as np
import Board
from Tree import *
import copy
class my_node(object):
    max_child_node = 10
    def __init__(self,pos=[],score=[]):
        #pos 和 score 都是一个list
        self.pos = pos
        self.score = score

    def pos_to_score(self,x,y):
        return self.score[self.pos.index([x,y])]
    def sort_self(self):
        new_pos = []
        order = np.argsort(self.score)
        self.score = sorted(self.score)
        for i in order:
            new_pos.append(self.pos[i])
        length = len(self.score)
        if length > self.max_child_node:
            self.score = self.score[length - self.max_child_node:]
            new_pos = new_pos[length - self.max_child_node:]
        self.pos = new_pos

    def pop(self):
        return [self.pos.pop(),self.score.pop()]

    def print_data(self):
        print(self.score,self.pos)


class alpha_beta(object):
    node_model = my_node()
    next_pos = []
    depth = 4
    cur_node = []
    defend_to_attack = 1
    dxdy = {0:[0,-1],1:[1,-1],2:[1,0],3:[1,1]}
    all_str = [["11111"],
               ["011110"],
               ["011112","0101110","0110110"],
               ["211112"],
               ["01110","010110"],
               ["001112","010112","011012","10011","10101","2011102"],
               ["21112"],
               ["0110","01010","010010"],
               ["000112","001012","010012","10001","2010102","2011002"],
               ["2112"],
               ["010","012"]]
    score_man = 0
    score_cpu = 0
    score_total = score_cpu - score_man
    dis = 1#范围相关的距离,这样可以不搜索太远的位置.
    def __init__(self,data,index,pre_pos):
        # self.node_child = []
        # for i in range(self.depth+1):
        #     self.node_child.append(my_node())
        self.pre_pos=pre_pos
        self.cur_node = []
        self.index = index
        self.data = data
        self.len_x = np.size(data,1)   #len_x = len_y = 15
        self.len_y = self.len_x
        self.cpu_is_first = [1,0][1] #1:电脑先下,0:选手先下
        self.position_score = [[0] * self.len_x for i in range(self.len_x)]
        self.position_score = np.array(self.position_score)
        for i in range(1, self.len_x // 2 + 2):
            self.position_score[i:self.len_x - i, i:self.len_x - i] += 1
    # function alphabeta(node, depth, α, β, maximizingPlayer) is
    # if depth = 0 or node is a terminal node then
    # return the heuristic value of node
    # if maximizingPlayer then
    #       value := −∞
    # for each child of node do
    #       value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
    #       α := max(α, value)
    # if α ≥ β then
    # break (* β cut-off *)
    # return value
    # else
    # value := +∞
    # for each child of node do
    # value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
    # β := min(β, value)
    # if α ≥ β then
    # break (* α cut-off *)
    # return value
    # (* Initial call *)
    # alphabeta(origin, depth, −∞, +∞, TRUE)
    def run(self):
        pos = self.get_res()
        # pos,score = self.alpha_beta(self.pre_pos,self.depth,float("-inf"),float("inf"),True)
        #根据分数来找位置.
        return pos

    def update_pos(self):
        #获取当前所有可以下的棋子的位置:
        temp = my_node([],[])
        for i in range(15):
            for j in range(15):
                if self.can_down(i,j):
                    score  = self.get_dir_score(i,j)
                    temp.pos.append([i,j])

                    temp.score.append(score)
                    # temp.print_data()
        temp.sort_self()

        return temp.pos,temp.score
    # def get_board_score(self):


    def alpha_beta(self,node,depth,alpha,beta,maximizingPlayer):
        #如果搜索到叶子结点了,也就是depth = 0 ,node 是叶子结点

        if depth == 0:

            t_score = 0
            k = -1
            for i,j in zip(range(len(self.cur_node)),self.cur_node):
                t_score += self.get_dir_score(j[0],j[1]) * k
                k = -k

            if self.cur_node.__len__() != 0:
                return self.cur_node[-1],t_score
            else:
                return [],t_score


        # self.cur_node.append(node)
        # print(self.cur_node)
        child,score = self.update_pos()
        print("child = {}".format(child))
        #只有第一次的时候才会更新
        if score[0] == float("inf"):
            return child[0],score[0]
        if self.next_pos == []:
            self.next_pos = child.copy()
            self.next_pos = self.next_pos[::-1]
            print("next_pos = {}".format(self.next_pos))
        if maximizingPlayer:
            # MAX 层 取 MIN层 的 最大值

            value = float("-inf")
            pos = []
            t_node = node
            while child.__len__() != 0:
                #使用了这个结点就要把这个结点直接移走,并且将data[node[0],node[1]] = index +self.depth -depth

                temp = child.pop()
                self.cur_node.append(temp)
                # print(self.cur_node)
                tx,ty = temp
                #index: cpu / index+1: man
                self.data[ty,tx] = self.index + depth % 2

                t_pos,t_value = self.alpha_beta(temp,depth-1,alpha,beta,False)
                self.cur_node.pop()
                if t_value > value:
                    value = t_value
                    pos = temp
                alpha = max(alpha,value)


                self.data[ty,tx] = 0
                # if t_pos != self.cur_node[-1]:
                # print(self.cur_node)

                if alpha >= beta:
                    break
            return pos,value
        else:
            value = float("inf")
            pos = []
            while child.__len__() != 0:

                temp = child.pop()
                tx,ty = temp
                self.cur_node.append(temp)
                # print(self.cur_node)

                #index: cpu / index+1: man
                self.data[ty,tx] = self.index + depth % 2

                t_pos,t_value = self.alpha_beta(temp,depth-1,alpha,beta,True)
                self.cur_node.pop()
                # print(self.cur_node)
                if t_value < value:
                    value = t_value
                    pos = temp
                beta = min(beta,value)

                self.data[ty,tx] = 0
                # if t_pos != self.cur_node[-1]:
                # print(self.cur_node)
                if alpha >= beta:
                    break
            return pos,value


    def alpha_beta1(self,node,depth,alpha,beta,maximizingPlayer,is_last_node):
        if depth != 0:
            child = self.update_pos()
        if depth == 0 or is_last_node:
            return self.cur_node.pop()

        if maximizingPlayer:
            value = float("-inf")
            pos = [-1,-1]
            while child.pos.__len__() != 0:
                #使用了这个结点就要把这个结点直接移走,并且将data[node[0],node[1]] = index +self.depth -depth
                temp = child.pop()
                self.cur_node.append(temp)
                is_last_node = False
                if child.pos.__len__() == 0:
                    is_last_node=True
                tx,ty = temp[0]
                self.data[ty,tx] = self.index + self.depth - depth

                [pos,t_value] = self.alpha_beta(temp[0],depth-1,alpha,beta,False,is_last_node)

                # self.cur_node.pop()
                if t_value > value:
                    value = t_value

                self.data[ty,tx] = 0
                alpha = max(alpha,value)

                if alpha >= beta:
                    break

            return pos,value
        else:
            value = float("inf")
            pos = [-1,-1]
            while child.pos.__len__() != 0:

                temp = child.pop()
                self.cur_node.append(temp)

                is_last_node = False
                if child.pos.__len__() == 0:
                    is_last_node=True
                tx,ty = temp[0]
                self.data[ty,tx] = self.index + self.depth - depth

                [pos,t_value] = self.alpha_beta(temp[0],depth-1,alpha,beta,True,is_last_node)

                # self.cur_node.pop()
                if t_value < value:
                    value = t_value

                self.data[ty,tx] = 0
                beta = min(beta,value)
                if alpha >= beta:
                    break
            return pos,value
















    # 用来判断当前的位置(x_pos,y_pos)周围1的距离内有没有子.
    # x_pos :int; y_pos:int;
    def in_board(self,x_pos,y_pos):
        if 0 <= x_pos < self.len_x and 0 <= y_pos < self.len_y:
            return True
        return False

    def can_down(self,x_pos,y_pos):
        #没有下的地方 and 有必要下的地方
        if self.data[y_pos,x_pos] != 0:
            return False
        left,top = x_pos-1,y_pos-1
        for i in range(left,left+2*self.dis+1):
            if i < 0 or i >= self.len_x:
                continue
            for j in range(top,top+2*self.dis+1):
                if  j < 0 or j >= self.len_y:
                    continue
                if self.data[j,i] != 0:
                    return True
        return False

    def get_res(self):
        total_score,total_pos = self.get_score_pos()
        for i in range(len(total_score)):
            print("{}->{}".format(total_pos[i],total_score[i]))
        # print("get_res(): total_score:{}".format(total_score))
        # print("get_res(): total_pos:{}",total_pos)
        temp = total_score.index(max(total_score))
        print("get_res(): temp:{}".format(temp))
        print(total_pos[temp])
        x,y = total_pos[temp]
        return x,y

    def get_score_pos(self):
        score = []
        pos = []
        for i in range(self.len_x):
            for j in range(self.len_y):
                if self.can_down(i,j):#debug (i,j)肯定在范围之内,只需要判断是不是有必要下在这个地方
                    temp = self.get_dir_score(i,j)
                    # print(i,j)
                    # print(temp)
                    score.append(temp)
                    pos.append([i,j])
        # print("score={}".format(score))
        return score,pos


    def get_board_res(self):
        #有待改进和测试,不加αβ的时候单层的效果没有单个子的评分的效果好.
        score = [[float("-inf")]*15 for i in range(15) ]

        for i in range(15):
            for j in range(15):
                if self.can_down(i,j):
                    score[j][i] = 0
        for i in range(15):
            for j in range(15):
                if score[j][i] == 0:
                    score[j][i] += self.get_dir_score(i,j)

        # print("score = {}".format(np.array(score)))
        max_score = np.max(score)
        y_max,x_max = np.where(score == max_score)
        # print("y_max = {},x_max = {}".format(y_max,x_max))
        return x_max[0],y_max[0]

    def get_board_socre(self):
        book = [[0]]
    def get_dir_score(self,x_pos,y_pos):

        score = float("-inf")
        for is_attack in (0,1):#0:进攻,1:防守
            temp = [""]*4
            for direction in range(4):

                tx,ty = x_pos,y_pos
                tx = tx - self.dxdy[direction][0]*14
                ty = ty - self.dxdy[direction][1]*14
                for i in range(29):

                    if not self.in_board(tx,ty):
                        temp[direction] += "3"
                    elif self.data[ty, tx] == 0:
                        if tx == x_pos and ty == y_pos:
                            temp[direction] += "1"
                        else:
                            temp[direction] += "0"
                    elif self.data[ty, tx] % 2 != is_attack:
                        temp[direction] += "2"
                    else:
                        temp[direction] += "1"

                    tx = tx + self.dxdy[direction][0]
                    ty = ty + self.dxdy[direction][1]
            #test:
            # if is_attack == 0:
            #     score.attack = self.str_to_score(temp)
            # else:
            #     score.defend = self.str_to_score(temp)
            score = max(self.str_to_score(temp),score)
            # score += self.str_to_score(temp)
        return score

    def str_to_score(self,astr):
        #活2眠2	            10
        #双活2	            100
        #活3眠3	            1000
        #双活3	            5000
        #活4/双冲4/冲4活3	    10000
        #先判断分数高的
        f = [[],[],[],[]]
        for i in range(4):
            for j in range(len(self.all_str)):
                f[i].append(self.in_astr(self.all_str[j],astr[i]))
        f = np.transpose(f).tolist()
        # temp = np.transpose(temp)
        # f = []
        # for i in range(len(temp)):
        # 	f.append(True in temp[i])
        if True in f[0]:#五连
            return float("inf")
        if True in f[1]:#活四
            return 10000
        if f[2].count(True) >=2:#双冲4
            return 10000
        if True in f[2] and True in f[4]:#冲4活3
            return 10000
        if f[4].count(True) >= 2:#双活3
            return 5000
        if True in f[4] and True in f[5]:#活3眠3
            return 1000
        if True in f[2]:#冲四
            return 500
        if True in f[4]:#活三
            return 200
        if f[6].count(True) >= 2:#双活2
            return 100
        if True in f[5]:#眠3
            return 50
        if True in f[7] and True in f[8]:#活2眠2
            return 10
        if True in f[7]:#活2
            return 5
        if True in f[8]:#眠2
            return 3
        if True in f[3] or True in f[6] or True in f[9]:#死四
            return -5
        else:
            return 0

    def in_astr(self,string,astr):
        for i in range(len(string)):
            if string[i] in astr or string[i][::-1] in astr:
                return True
        return False




    def test(self):

        # position = self.get_board_res()
        position  = self.get_res()
        # print("test():获取得结果是:({})".format(position))
        return position

if __name__ == "__main__":
    data =[[ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0,11, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0,10, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 7, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 6, 5, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 2, 0, 3, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 7, 1,12, 14, 16, 18,0,0],
           [ 0,0,0,0,0,0,0, 4, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 13,0,0],
           [ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0,0,0],
           [ 0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0,0,0]]
    pos = [12,9]
    data = np.array(data)
    t = alpha_beta(data,15,pos)
    s = t.get_dir_score(13,6)
    print(s)

    # data =[[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,11,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,10,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,14,8,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,6,5,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,2,0,3,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,7,1,12,9,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,4,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,0,0,0,0,0,13,0,0],
    #        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    # data = np.array(data)
    # t = alpha_beta(data,15)
    # s = t.get_dir_score(11,7)
    #
    #
    # print(s)
