import tkinter as tk
from tkinter import messagebox
from tiktaktoe import TicTacToe, Player

EMPTY = None
X = "X"
O = "O"

class TicTacToeGUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe')
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.initialize_buttons()

    def initialize_buttons(self):
        for i in range(3):
            for j in range(3):
                # Füge den Text mit Reihen- und Spaltennummer hinzu
                self.buttons[i][j] = tk.Button(self.window, height=4, width=8,
                                            font=('Arial', 20),
                                            command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)


    def on_button_click(self, x, y):
        if self.game.board.canvas[x][y] == EMPTY and not self.game.board.is_terminal():
            # Erlaube den Zug nur, wenn das Feld leer ist und das Spiel nicht vorbei ist
            self.make_move(x, y, self.game.current_player)
            if not self.game.board.is_terminal():
                self.game.switch_player()  # Wechsle den Spieler
                self.window.after(500, self.ai_move)  # Füge eine kurze Verzögerung ein, bevor die KI ihren Zug macht
            
     
           

    def ai_move(self):
        print(self.game.board.canvas)
        ai_move = self.game.ai_player.action(self.game.board)
        if ai_move:
            self.make_move(ai_move[0], ai_move[1], self.game.current_player)
            if not self.game.board.is_terminal():
                self.game.switch_player()  # Wechsle zurück zum menschlichen Spieler

    def make_move(self, x, y, player):
        try:
            self.game.board.make_move(player, (x, y))
            self.buttons[x][y]['text'] = player
            winner = self.game.check_winner()
            if winner or self.game.board.is_terminal():
                end_message = f"Spieler {winner} hat gewonnen!" if winner else "Unentschieden!"
                messagebox.showinfo("Spiel Ende", end_message)
                self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Fehler", str(e))

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.ai_player = Player(O)  # Initialisiere die KI für den Spieler O
    gui = TicTacToeGUI(game)
    gui.start()
