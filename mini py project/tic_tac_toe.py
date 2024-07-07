import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human_player = 'X'
        self.ai_player = 'O'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_buttons()

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=' ', font=('Arial', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.human_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def human_move(self, row, col):
        if self.buttons[row][col]['text'] == ' ':
            self.buttons[row][col]['text'] = self.human_player
            self.board[row][col] = self.human_player
            if self.check_winner() or self.is_board_full():
                self.end_game()
            else:
                self.ai_move()

    def ai_move(self):
        move = self.best_move()
        self.buttons[move[0]][move[1]]['text'] = self.ai_player
        self.board[move[0]][move[1]] = self.ai_player
        if self.check_winner() or self.is_board_full():
            self.end_game()

    def end_game(self):
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
        self.root.quit()

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != ' ':
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != ' ':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != ' ':
            return self.board[0][2]
        return None

    def is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner()
        if winner == self.human_player:
            return -1
        elif winner == self.ai_player:
            return 1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = self.ai_player
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = self.human_player
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def best_move(self):
        best_score = float('-inf')
        move = (0, 0)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.ai_player
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
