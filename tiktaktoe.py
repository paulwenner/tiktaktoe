#Globale Variablen zur Vereinfachung
EMPTY = None
X = "X"
O = "O"

class TicTacToe():
    def __init__(self):
        #Spielboard initialisieren
        self.board = Board()
        self.current_player = X

    def switch_player(self):
        #Spieler bestimmen, je nach Zug
        if self.current_player == X:
            self.current_player = O
        else:
            self.current_player = X

    def play_game(self):
        # Hauptfunktion für den Spielablauf
        # Das Spiel läuft solange, bis ein Gewinner ermittelt oder das Brett voll ist
        while not self.board.is_terminal():
            # Menschlicher Spieler (X)
            if self.current_player == X:
                print(self.current_player)
                x = int(input("x:"))  # Eingabe der x-Koordinate
                y = int(input("y:"))  # Eingabe der y-Koordinate
                self.board.make_move(self.current_player, (x, y))  # Zug auf dem Brett ausführen
                self.board.print_board()  # Aktuellen Stand des Bretts ausgeben
                if self.board.get_winner():  # Überprüfung, ob es einen Gewinner gibt
                    print(self.board.get_winner())
                    break
                self.switch_player()  # Wechsel zum nächsten Spieler

            # KI-Spieler (O)
            else:
                ai_player = Player(self.current_player)
                action = ai_player.action(self.board)  # Bestimmung des Zugs durch die KI
                self.board.make_move(self.current_player, action)  # Zug ausführen
                self.board.print_board()  # Brett ausgeben
                if self.board.get_winner():  # Überprüfung auf Gewinner
                    print(self.board.get_winner())
                    break
                self.switch_player()  # Spieler wechseln

    def check_winner(self):
        # Ermittelt den Gewinner, wenn vorhanden
        return(self.board.get_winner())



class Board():
    def __init__(self):
        #Board initilisieren
        self.canvas = [[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]

    def print_board(self):
        #Board ausgeben
        print(f"\n{self.canvas[0]}\n{self.canvas[1]}\n{self.canvas[2]}")

    def make_move(self, player, action):
        #Spieler 'player' macht Zug 'action'
        x, y = action
        
        if self.canvas[x][y] == EMPTY:
            self.canvas[x][y] = player
        else:
            raise ValueError("Feld bereits besetzt")

    def get_possible_actions(self):
        #Was sind die möglichen nächsten Aktionen
        actions = []
        for x, row in enumerate(self.canvas):
            for y, item in enumerate(row):
                if item == EMPTY:
                    actions.append((x, y))
        return actions

    def get_winner(self):
        #Gibt es einen Gewinner und wenn ja wer
        canvas = self.canvas

        # Überprüfe Diagonalen
        if canvas[0][0] == canvas[1][1] == canvas[2][2] != EMPTY:
            return canvas[1][1]
        if canvas[0][2] == canvas[1][1] == canvas[2][0] != EMPTY:
            return canvas[1][1]

        # Überprüfe Reihen und Spalten
        for i in range(3):
            if canvas[i][0] == canvas[i][1] == canvas[i][2] != EMPTY:
                return canvas[i][0]
            if canvas[0][i] == canvas[1][i] == canvas[2][i] != EMPTY:
                return canvas[0][i]

        return None

    def is_terminal(self):
        #Ist das Spiel vorbei bzw. sind alle Felder besetzt
        if self.get_winner() is not None:
            return True
        for row in self.canvas:
            if EMPTY in row:
                return False
        return True

    def result(self, player, action):
        #Funktion für die KI
        #Was wäre das entstehende Board, wenn man den Spielzug 'action' machen würde
        new_board = Board()
        new_board.canvas = [row[:] for row in self.canvas]
        new_board.make_move(player, action)
        return new_board

    def utility(self):
        #Bewertet den Zustand des Bretts:
        #Für einen Sieg von X -> 1 für einen Sieg von O -> -1, für ein Unentschieden -> 0
        #Wichtig für den Minimax algorithmus
        winner = self.get_winner()
        if winner == X:
            return 1
        elif winner == O:
            return -1
        else:
            return 0




class Player(): #KI Spieler
    def __init__(self, player):
        self.player = player #Initialisierung des Spielers

    def action(self, board):
        #Bestimmung des bestmöglichen Zuges durch Minimax algorithmus
        _, action = self.minimax(board, self.player)
        return action

    def minimax(self, board, player):
        #Mnimax Implementierung
        #Falls das Spiel vorbei ist, gib es keinen bestmöglichen Zug mehr
        if board.is_terminal():
            return board.utility(), None

        #Falls self.player = X
        if player == X:
            best_val = float('-inf') #Einrichtung der Variablen
            best_action = None 
            for action in board.get_possible_actions(): #Alle möglichen Spielzüge ermitteln
                new_board = board.result(player, action) #Ein aus einem Spielzug entstehendes Board ermitteln
                val, _ = self.minimax(new_board, O) #Rekursive Funktion um mögliche Spielausgänge aus dem entstehenden Board zu ermitteln
                if val > best_val: #Logische Aktualisierung um die beste Aktion zu finden 
                    best_val = val
                    best_action = action
            return best_val, best_action 
        else:
            best_val = float('inf')
            best_action = None
            for action in board.get_possible_actions():
                new_board = board.result(player, action)
                val, _ = self.minimax(new_board, X)
                if val < best_val:
                    best_val = val
                    best_action = action
            return best_val, best_action



if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()




















