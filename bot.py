import random
from score import Score
import constants as const
import time


class Bot():

    def __init__(self):
        self.board = []
        self.player = []
        self.loop = 0
        self.score = Score()

    def out_of_range(self, r, c):
        if 0 <= r <= 7 and 0 <= c <= 7:
            return False
        return True

    def it_is_bot(self, r, c):
        if not self.out_of_range(r, c) and 1 <= self.board[r][c] <= 8:
            return True
        return False

    def it_is_player(self, r, c):
        if not self.out_of_range(r, c) and 9 <= self.board[r][c] <= 16:
            return True
        return False

    def it_is_blank(self, r, c):
        if not self.out_of_range(r, c) and self.board[r][c] == 0:
            return True
        return False

    def basic_cannot_move(self, dr, dc):
        if (dr == 0 or dc == 0 or abs(dr) != abs(dc)):
            return True
        return False

    def get_character(self, number):
        return self.player[number].character

    def can_eat(self, r, c):
        if self.get_character(self.board[r][c]) == 'w':
            if self.it_is_player(r + 1, c + 1) and self.it_is_blank(r + 2, c + 2):
                return r + 2, c + 2, r + 1, c + 1,  True
            elif self.it_is_player(r + 1, c - 1) and self.it_is_blank(r + 2, c - 2):
                return r + 2, c - 2, r + 1, c - 1, True

        elif self.get_character(self.board[r][c]) == 'W':
            for i, j in const.DIR:
                for ct in range(1, 7):
                    if self.it_is_player(r + i * ct, c + j * ct):
                        if self.it_is_blank(r + i * (ct + 1), c + j * (ct + 1)):
                            return r + i * (ct + 1), c + j * (ct + 1), r + i * ct, c + j * ct, True
                        else:
                            break
                    elif self.it_is_bot(r + i * ct, c + j * ct):
                        break
        return 0, 0, 0, 0, False

    def player_can_eat(self, r, c, r_w, c_w):
        r_p, c_p = r_w + 1, c_w + 1
        if self.it_is_player(r_p, c_p):
            if c_p - c_w == c_w - c == 1:
                return True
            elif self.it_is_player(r + 2, c) and self.it_is_blank(r, c - 2):
                return True

        r_p, c_p = r_w + 1, c_w - 1
        if self.it_is_player(r_p, c_p):
            if c_p - c_w == c_w - c == -1:
                return True
            elif self.it_is_player(r + 2, c) and self.it_is_blank(r, c + 2):
                return True

        return False

    def can_walk(self, r, c):
        if self.get_character(self.board[r][c]) == 'w':
            if self.it_is_blank(r + 1, c + 1) and not self.player_can_eat(r, c, r + 1, c + 1):
                return r + 1, c + 1, True, False
            elif self.it_is_blank(r + 1, c - 1) and not self.player_can_eat(r, c, r + 1, c - 1):
                return r + 1, c - 1, True, False
            elif self.it_is_blank(r + 1, c + 1) and self.player_can_eat(r, c, r + 1, c + 1):
                return r + 1, c + 1, True, True
            elif self.it_is_blank(r + 1, c - 1) and self.player_can_eat(r, c, r + 1, c - 1):
                return r + 1, c - 1, True, True

        elif self.get_character(self.board[r][c]) == 'W':
            for i, j in const.DIR:
                for ct in range(1, 7):
                    if self.it_is_blank(r + i * ct, c + j * ct):
                        return r + i * ct, c + j * ct, True, False
                    else:
                        break
        return 0, 0, False, False

    def new_board(self):
        list_node = []
        list_node.append(Node())
        score = 0
        for r in range(0, 8):
            for c in range(0, 8):
                if not self.it_is_bot(r, c):
                    continue
                eat_status = False
                walk_status = False
                player_eat = False
                r_e, c_e, r_eat, c_eat, eat_status = self.can_eat(r, c)
                r_w, c_w, walk_status, player_eat = self.can_walk(r, c)

                if eat_status:
                    score = 4
                elif walk_status and not player_eat and self.loop == 0:
                    score = 3
                elif walk_status and self.loop == 0:
                    score = 2

                if score >= list_node[-1].score and (walk_status or eat_status):
                    if score > list_node[-1].score:
                        while len(list_node) > 0:
                            if list_node[-1].score == score:
                                break
                            list_node.pop()
                    if score == 3 or score == 2:
                        list_node.append(
                            Node(self.board[r][c], score, r, c, r_w, c_w))
                    elif score == 4:
                        list_node.append(
                            Node(self.board[r][c], score, r, c, r_e, c_e, r_eat, c_eat))

        while len(list_node) > 0 and list_node[-1].r_current == 0 and list_node[-1].c_current == 0:
            list_node.pop()
        if len(list_node) > 0:
            # index = random.randrange(len(list_node))
            index = -1
            self.board[list_node[index].r_origin][
                list_node[index].c_origin] = 0
            if list_node[index].score == 4:
                self.board[list_node[index].r_eat][list_node[index].c_eat] = 0
                self.loop = 1
                self.score.increase('b')
            self.board[
                list_node[index].r_current][list_node[index].c_current] = list_node[index].number
        else:
            if self.loop == 0:
                self.score.increase('p')
            self.loop = 0

    def print_board(self):
        for i in range(0, 8):
            print(self.board[i])

    def play(self, board_origin, player_origin, score):
        self.board = board_origin
        self.player = player_origin
        self.loop = 0
        self.new_board()
        self.score = score
        while self.loop > 0:
            self.new_board()
        return self.board


class Node():

    def __init__(self, number=0, score=0, r_origin=0, c_origin=0, r_current=0, c_current=0, r_eat=0, c_eat=0):
        self.number = number
        self.score = score
        self.r_origin = r_origin
        self.c_origin = c_origin
        self.r_current = r_current
        self.c_current = c_current
        self.r_eat = r_eat
        self.c_eat = c_eat
