import sys

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board as flat list
        self.current_winner = None
        
    def print_board(self):
        """Display the current board state"""
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| '.join(row))
            if row != self.board[6:]:
                print('-' * 3)
    
    def available_moves(self):
        """Return list of available moves (empty positions)"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        """Check if board has empty squares"""
        return ' ' in self.board
    
    def make_move(self, square, letter):
        """Make a move on the board"""
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square):
        """Check if the move at square creates a winner"""
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind + 1)*3]
        if all([spot == self.board[square] for spot in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind + (i * 3)] for i in range(3)]
        if all([spot == self.board[square] for spot in column]):
            return True
        
        # Check diagonals
        if square % 2 == 0:  # Possible diagonal
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == self.board[square] for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == self.board[square] for spot in diagonal2]):
                return True
        return False

def minimax(state, player):
    """Minimax algorithm with Alpha-Beta pruning"""
    max_player = 'X'  # AI player
    other_player = 'O' if player == 'X' else 'X'
    
    if state.current_winner:
        return {'position': None,
                'score': 1 * (len(state.available_moves()) + 1) if state.current_winner == max_player else -1 * (len(state.available_moves()) + 1)}
    
    elif not state.empty_squares():
        return {'position': None, 'score': 0}
    
    if player == max_player:
        best = {'position': None, 'score': -float('inf')}
    else:
        best = {'position': None, 'score': float('inf')}
    
    for possible_move in state.available_moves():
        state.make_move(possible_move, player)
        sim_score = minimax(state, other_player)
        state.board[possible_move] = ' '  # Undo move
        state.current_winner = None
        sim_score['position'] = possible_move
        
        if player == max_player:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    
    return best

class Game:
    def __init__(self):
        self.board = TicTacToe()
        self.human_letter = 'X'
        self.ai_letter = 'O'
    
    def setup_game(self):
        """Let player choose symbol and who goes first"""
        print("Welcome to Tic-Tac-Toe!")
        print("Choose your symbol (X or O):")
        while True:
            choice = input("Enter X or O: ").upper()
            if choice in ['X', 'O']:
                self.human_letter = choice
                self.ai_letter = 'O' if choice == 'X' else 'X'
                break
            print("Invalid choice! Choose X or O.")
        
        print(f"\nYou are {self.human_letter}, AI is {self.ai_letter}")
        
        first_move = input("\nDo you want to go first? (y/n): ").lower()
        return first_move == 'y'
    
    def human_move(self):
        """Handle human player's move"""
        while True:
            square = input("Enter your move (0-8): ")
            try:
                square = int(square)
                if square not in self.board.available_moves():
                    raise ValueError
                return square
            except (ValueError, IndexError):
                print("Invalid move! Choose an empty position (0-8)")
    
    def ai_move(self):
        """AI makes optimal move using minimax"""
        print("AI is thinking...")
        move = minimax(self.board, self.ai_letter)['position']
        self.board.make_move(move, self.ai_letter)
        print(f"AI plays at position {move}")
    
    def display_board_with_numbers(self):
        """Show board with position numbers"""
        numbers = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in numbers:
            print('| '.join(row))
            print('-' * 3)
    
    def play(self):
        """Main game loop"""
        self.display_board_with_numbers()
        print()
        
        human_first = self.setup_game()
        current_player = self.human_letter if human_first else self.ai_letter
        
        while True:
            self.board.print_board()
            print()
            
            if current_player == self.human_letter:
                square = self.human_move()
                self.board.make_move(square, self.human_letter)
            else:
                self.ai_move()
            
            if self.board.winner(square):
                self.board.print_board()
                print(f"\n{'You' if self.board.current_winner == self.human_letter else 'AI'} wins!")
                break
            
            if not self.board.empty_squares():
                self.board.print_board()
                print("\nIt's a tie!")
                break
            
            current_player = self.ai_letter if current_player == self.human_letter else self.human_letter
        
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again == 'y':
            print("\n" + "="*30 + "\n")
            new_game = Game()
            new_game.play()

if __name__ == "__main__":
    game = Game()
    game.play()