from random import randint
from typing import List, Tuple
import pygame


EMPTY = 0
UP, LEFT = 1, 1
DOWN, RIGHT = -1, -1

class Board:
    def __init__(self, x_size: int, y_size: int) -> None:
        self.x_size = x_size
        self.y_size = y_size
        self.x_board: List[List[int]] = [[EMPTY for _ in range(self.x_size)] for _ in range(self.y_size)]
        self.add_random_number()

    def __str__(self) -> str:
        ret_str = ""
        for y in range(len(self.x_board)):
            ret_str += "-" * (2 * len(self.x_board) + 1) + "\n"
            
            for x in range(len(self.x_board[y])):
                ret_str += f"|{self.x_board[y][x]}"
                if x == len(self.x_board[y]) - 1:
                    ret_str += "|\n"
            
            if y == len(self.x_board) - 1:
                ret_str += "-" * (2 * len(self.x_board) + 1) + "\n"
        return ret_str

    def print_board(self) -> None:
        print(self)

    def check_game_over(self) -> bool:
        for y in range(len(self.x_board)):
            for x in range(len(self.x_board[y])):
                if self.x_board[y][x] == EMPTY \
                or (x + 1 < len(self.x_board[y]) and self.x_board[y][x] == self.x_board[y][x + 1]) \
                or (x - 1 >= 0 and self.x_board[y][x] == self.x_board[y][x - 1]) \
                or (y + 1 < len(self.x_board) and self.x_board[y][x] == self.x_board[y + 1][x]) \
                or (y - 1 >= 0 and self.x_board[y][x] == self.x_board[y - 1][x]):
                    return False
        return True

    def add_random_number(self) -> None:
        free_positions: List[Tuple[int, int]] = []
        for y in range(len(self.x_board)):
            for x in range(len(self.x_board[y])):
                if self.x_board[y][x] == EMPTY:
                    free_positions.append((y, x)) 
        if len(free_positions) == 0:
            return None
        y, x = free_positions[randint(0, len(free_positions) - 1)]
        self.x_board[y][x] = 2

    def horizontal_move(self, direction: int) -> bool:
        ret_val = False
        for row in self.x_board:
            ret_val = self.slide(row, direction) or ret_val
        return ret_val
        

    def vertical_move(self, direction: int) -> bool:
        ret_val = False
        for x in range(len(self.x_board[0])):
            actual_col = []
            for y in range(len(self.x_board)):
                actual_col.append(self.x_board[y][x])
            ret_val = self.slide(actual_col, direction) or ret_val
            for y in range(len(actual_col)):
                self.x_board[y][x] = actual_col[y]
        return ret_val

    def slide(self, row: List[int], direction: int) -> bool:
        ret_val = False
        func = (lambda x: x < len(row)) if direction == LEFT else (lambda x: x >= 0)

        editable_x = 0 if direction == LEFT else len(row) - 1
        actual_x = 1 if direction == LEFT else len(row) - 2
        while func(actual_x):
            if editable_x == actual_x:
                actual_x += direction
                continue

            if row[actual_x] == EMPTY:
                actual_x += direction

            elif row[editable_x] == EMPTY:
                row[editable_x] = row[actual_x]
                row[actual_x] = EMPTY
                actual_x += direction
                ret_val = True
            else:
                if row[editable_x] == row[actual_x]:
                    row[editable_x] += row[actual_x]
                    row[actual_x] = EMPTY
                    actual_x += direction
                    ret_val = True

                editable_x += direction
        return ret_val

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (30,144,255)
GREY = (169,169,169)

class App:
    def __init__(self, height: int, width: int) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.height = self.window.get_height()
        self.width = self.window.get_width()
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.x_size = 3
        self.y_size = 3
        self.board = Board(self.x_size, self.y_size)
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 75)
        self.font_end = pygame.font.SysFont("Arial", 150)
        self.directions = {pygame.K_w: UP, pygame.K_s: DOWN, pygame.K_a: LEFT, pygame.K_d: RIGHT}
        self.game_over = False

    def main_loop(self) -> None:
        self.redraw()
        while True:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.VIDEORESIZE:
                    self.height = self.window.get_height()
                    self.width = self.window.get_width()
                    self.redraw()
                elif not self.game_over and event.type == pygame.KEYDOWN:
                    direction = self.directions.get(event.key, None)
                    if direction is not None:
                        if event.key == pygame.K_w or event.key == pygame.K_s:
                            if self.board.vertical_move(direction):
                                self.board.add_random_number()
                                if self.board.check_game_over():
                                    print("Game_OVER")
                                    self.game_over = True
                                self.redraw()
                        else:
                            if self.board.horizontal_move(direction):
                                self.board.add_random_number()
                                if self.board.check_game_over():
                                    print("Game_OVER")
                                    self.game_over = True
                                self.redraw()
                        
                        
    def draw_game_over(self) -> None:
        text1 = self.font.render(f"GAME OVER", True, WHITE, BLACK)
        text2 = self.font.render(f"SCORE: {self.score}", True, WHITE, BLACK)
        x1, y1 = text1.get_size()
        x2, y2 = text2.get_size()
        self.window.blit(text1, (self.width / 2 - x1 / 2, self.height / 2 - y1 / 2))
        self.window.blit(text2, (self.width / 2 - x2 / 2, self.height / 2 - y2 / 2 + y2))
            
    def redraw(self) -> None:
        if self.game_over:
            self.draw_game_over()
            pygame.display.flip()
            return
        self.window.fill(BLACK)
        for row in range(len(self.board.x_board)):
            for col in range(len(self.board.x_board[row])):
                self.draw_field(col, row)
                if self.board.x_board[row][col] != EMPTY:
                    self.draw_number(col, row, self.board.x_board[row][col])
                    
        pygame.display.flip()

    def draw_field(self, col: int, row: int) -> None:
        pygame.draw.rect(self.window, RED, [self.width / self.x_size * col, self.height / self.y_size * row, self.width / self.x_size, self.height / self.y_size], width=10)

    def draw_number(self, col: int, row: int, num: int) -> None:
        text = self.font.render(f"{num}", True, WHITE)
        self.window.blit(text, (self.width / self.x_size * col + self.width / self.x_size / 2, self.height / self.y_size * row + self.height / self.y_size / 2))

    def refresh_window(self) -> None:
        self.window.blit(pygame.Surface())


App(500, 500).main_loop()
