import pygame
import sys
import random


class Board:
    def __init__(self,height, width):
        self.HEIGHT = height
        self.WIDTH = width
        self.GRID_SIZE = 3
        self.CELL_SIZE = self.HEIGHT//self.GRID_SIZE
        self.LINE_WIDTH = 5

        self.board = [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def draw_grid(self):
        for i in range(1,self.GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (i * self.CELL_SIZE, 0), (i * self.CELL_SIZE, self.HEIGHT), self.LINE_WIDTH)
            pygame.draw.line(self.screen, (255, 255, 255), (0, i * self.CELL_SIZE), (self.WIDTH, i * self.CELL_SIZE), self.LINE_WIDTH)

    def draw_xo(self, row, col):  
        if self.board[row][col] == 'X':
             pygame.draw.line(self.screen, "red", ((col*self.CELL_SIZE)+30, (row*self.CELL_SIZE)+30) , (((col+1)*self.CELL_SIZE)-30, ((row+1)*self.CELL_SIZE)-30), 5)
             pygame.draw.line(self.screen, "red", (((col+1)*self.CELL_SIZE)-30, (row*self.CELL_SIZE)+30), ((col*self.CELL_SIZE)+30, ((row+1)*self.CELL_SIZE)-30), 5)

        elif self.board[row][col] == 'O':
             pygame.draw.circle(self.screen, "yellow",(((col*self.CELL_SIZE)+self.CELL_SIZE//2), ((row*self.CELL_SIZE)+self.CELL_SIZE//2)), (self.CELL_SIZE//2)-30, 5)

    def update_board(self):
        self.draw_grid()
        for row in range(3):
            for col in range(3):
                self.draw_xo(row, col)

class Logic:
    def __init__(self, board):
        self.board = board

    def check_win(self):
        # linear pattern
        for i in range(self.board.GRID_SIZE):
            if all(self.board.board[i][j] == 'X' for j in range(self.board.GRID_SIZE)) or all(self.board.board[j][i] == 'X' for j in range(self.board.GRID_SIZE)):
                return 'X'
            if all(self.board.board[i][j] == 'O' for j in range(self.board.GRID_SIZE)) or all(self.board.board[j][i] == 'O' for j in range(self.board.GRID_SIZE)):
                return 'O'
        # Diagonal match
        if all(self.board.board[i][i] == 'X' for i in range(self.board.GRID_SIZE)) or all(self.board.board[i][self.board.GRID_SIZE - i - 1] == 'X' for i in range(self.board.GRID_SIZE)):
            return 'X'
        elif  all(self.board.board[i][i] == 'O' for i in range(self.board.GRID_SIZE)) or all(self.board.board[i][self.board.GRID_SIZE - i - 1] == 'O' for i in range(self.board.GRID_SIZE)):
                return 'O'
        # tie
        if all(self.board.board[i][j] != ' ' for i in range(self.board.GRID_SIZE) for j in range(self.board.GRID_SIZE)):
            return 'Tie'
        return None


class AI:
    def __init__(self):
        self.temp_board = Board(500, 500)
        self.logic = Logic(self.temp_board) 

    def evaluate(self, board):
        for col in range(3):
            if all(board[row][col] == 'X' for row in range(3)):
                return 10
            if all(board[row][col] == 'O' for row in range(3)):
                return -10
            
        for row in board:
            if all(cell == 'X' for cell in row):
                return 10
            if all(cell == 'O' for cell in row):
                return -10
            
        if all(board[i][i] == 'X' for i in range(3)) or all(board[i][2 - i] == 'X' for i in range(3)):
            return 10
        elif all(board[i][i] == 'O' for i in range(3)) or all(board[i][2 - i] == 'O' for i in range(3)):
            return -10
        return 0
    
    def is_terminal(self, board):
      
        is_empty = any(cell == ' ' for row in board for cell in row)
        is_win = False if self.logic.check_win() == None else True
        return not is_empty or is_win
    
        
    def minmax(self,board, depth, is_maximizing, player, alpha, beta):

        score = self.evaluate(board)
        if score == 10:
            return score - depth
        elif score == -10:
            return score + depth
        elif self.is_terminal(board):
            return 0

        if is_maximizing:        
                opponent = 'X' if player == 'O' else 'O'
                max_eval = float('-inf')
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ' ':
                            board[i][j] = opponent
                            eval_score = self.minmax(board, depth + 1, not is_maximizing, opponent, alpha, beta)
                            max_eval = max(max_eval, eval_score)
                            alpha = max(alpha, eval_score)
                            board[i][j] = ' '
                            if beta <= alpha:
                                break  #                      
                return max_eval
        
        else:
            min_eval = float('inf')
            opponent = 'X' if player == 'O' else 'O'
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = opponent
                        eval_score = self.minmax(board, depth + 1, not is_maximizing, opponent, alpha, beta)
                        min_eval = min(min_eval, eval_score)      
                        beta = min(beta, eval_score)
                        board[i][j] = ' '
                        if beta <= alpha:
                            break  # Alpha cutoff
            return min_eval
                
    def find_best_move(self, board, current_player):
        if all(cell == ' ' for row in board for cell in row):
            row = random.randint(0,2)
            col = random.randint(0,2)
            return (row,col)
        
        else:
            best_val = float('-inf') if current_player == 'X' else float('inf')
            best_move = (-1, -1)

            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = current_player
                        if current_player == 'X':
                            move_val = self.minmax(board, -1, False, current_player,float('-inf'), float('inf'))
                        else:
                            move_val = self.minmax(board, 0, True, current_player,float('-inf'), float('inf'))
                        board[i][j] = ' '  # Undo the move

                        if (current_player == 'X' and move_val > best_val) or (current_player == 'O' and move_val < best_val):
                            best_move = (i, j)
                            best_val = move_val
            return best_move
        
class Game:

    def __init__(self, board):
        self.board = board
        self.PLAYER = 0
        self.AI = 1

        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.board.WIDTH, self.board.HEIGHT))
        self.clock = pygame.time.Clock()
        self.ai = AI()

    def choose_icon(self):
        
        player = None
        ai = None
        not_clicked = True
        while not_clicked:
            
            self.screen.fill((0, 0, 0))
            text = self.font.render("Press X/O for choosing pieces ", True, (255, 255, 255))                   
            self.screen.blit(text, (self.board.WIDTH // 2 - text.get_width() // 2, self.board.HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        player = 'X'
                        ai = 'O'
                        not_clicked = False

                    if event.key == pygame.K_o:
                        player = 'O'
                        ai = 'X'
                        not_clicked = False
        return player, ai

    def start_game(self):

        self.board.board = [[' ' for _ in range(self.board.GRID_SIZE)] for _ in range(self.board.GRID_SIZE)]
        self.logic = Logic(self.board)
        player, ai = self.choose_icon()
        if player == 'X':
            turn = self.PLAYER
        else:
            turn = self.AI
        self.screen.fill((0, 0, 0))

        running = True
        game_over = False
        # While the loop is true
        while running and player is not None and ai is not None:
            pygame.event.pump()
            self.board.update_board()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if turn == self.PLAYER and game_over == False:
                        row = event.pos[1] // self.board.CELL_SIZE
                        col = event.pos[0] // self.board.CELL_SIZE
                        if 0 <= row < self.board.GRID_SIZE and 0 <= col < self.board.GRID_SIZE and self.board.board[row][col] == ' ':
                            self.board.board[row][col] = player
                            turn = self.AI
                            self.board.update_board()

            pygame.display.flip()
            self.board.update_board()
            # pygame.time.delay(1000)
            result = self.logic.check_win()
            if result:
                game_over = True
                if result == "Tie":
                    text = self.font.render(f"Tied! Click to restart.", True, (255, 255, 255))
                else:
                    text = self.font.render(f"{result} wins! Click to restart.", True, (255, 255, 255))

                self.screen.blit(text, (self.board.WIDTH // 2 - text.get_width() // 2, self.board.HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()

                restart = False
                while not restart:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            restart = True
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            board = [[' ' for _ in range(self.board.GRID_SIZE)] for _ in range(self.board.GRID_SIZE)]
                            restart = True
                            game_over = False
                            self.screen.fill((0, 0, 0))
                            self.start_game()
                            running = False

            if turn == self.AI and game_over == False:
                row, col = self.ai.find_best_move(self.board.board, ai)
                if 0 <= row < self.board.GRID_SIZE and 0 <= col < self.board.GRID_SIZE and self.board.board[row][col] == ' ':
                    self.board.board[row][col] = ai
                    turn = self.PLAYER
                self.board.update_board()

            self.clock.tick(30)  # Limit to 30 frames per second
            self.board.update_board()

        pygame.quit()

        
if __name__ == "__main__":
    board = Board(500, 500)
    game = Game(board)
    game.start_game()

