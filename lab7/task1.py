import math

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'O'  # Human player starts
        self.ai_player = 'X'
        self.human_player = 'O'
    
    def print_board(self):
        for i in range(3):
            print(' | '.join(self.board[i]))
            if i < 2:
                print('-' * 9)
    
    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def get_empty_positions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    positions.append((i, j))
        return positions
    
    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        
        if winner == self.ai_player:
            return 10 - depth
        if winner == self.human_player:
            return depth - 10
        if self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for row, col in self.get_empty_positions():
                self.board[row][col] = self.ai_player
                score = self.minimax(depth + 1, False)
                self.board[row][col] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row, col in self.get_empty_positions():
                self.board[row][col] = self.human_player
                score = self.minimax(depth + 1, True)
                self.board[row][col] = ' '
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        
        for row, col in self.get_empty_positions():
            self.board[row][col] = self.ai_player
            score = self.minimax(0, False)
            self.board[row][col] = ' '
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    def play(self):
        print("Welcome to Tic-Tac-Toe!")
        print("You are O and the AI is X")
        print("Enter your moves as row and column indices (0-2)")
        
        while True:
            self.print_board()
            
            if self.current_player == self.human_player:
                while True:
                    try:
                        row, col = map(int, input("Enter row and column (0-2): ").split())
                        if 0 <= row <= 2 and 0 <= col <= 2:
                            if self.make_move(row, col, self.human_player):
                                break
                            else:
                                print("That position is already occupied. Try again.")
                        else:
                            print("Indices must be between 0 and 2. Try again.")
                    except ValueError:
                        print("Please enter two numbers separated by a space. Try again.")
            else:
                print("AI is thinking...")
                row, col = self.get_best_move()
                self.make_move(row, col, self.ai_player)
                print(f"AI placed X at {row}, {col}")
            
            winner = self.check_winner()
            if winner:
                self.print_board()
                if winner == self.human_player:
                    print("Congratulations! You won!")
                else:
                    print("AI wins!")
                break
            
            if self.is_board_full():
                self.print_board()
                print("It's a draw!")
                break
            
            self.current_player = self.ai_player if self.current_player == self.human_player else self.human_player

# Start the game
if __name__ == "__main__":
    game = TicTacToe()
    game.play()