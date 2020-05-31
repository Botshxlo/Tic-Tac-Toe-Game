# DO NOT MODIFY THIS FILE

from GameServer import *
from random import *

class OXOGameServer(GameServer):
    
    def __init__(self):
        GameServer.__init__(self)

    def is_move_valid(self,i):
        return i.strip().isdigit() and 0 <= int(i) < BOARD_SIZE and self.board[int(i)] == ' '
    
    def is_board_full(self):
        return ' ' not in self.board
        
    def is_game_finished(self): # 048, 012, 036, 147, 246, 258, 345, 678
        if (self.board[0] != ' ' and self.board[0] == self.board[4] and self.board[4] == self.board[8]) \
        or (self.board[0] != ' ' and self.board[0] == self.board[1] and self.board[1] == self.board[2]) \
        or (self.board[0] != ' ' and self.board[0] == self.board[3] and self.board[3] == self.board[6]) \
        or (self.board[1] != ' ' and self.board[1] == self.board[4] and self.board[4] == self.board[7]) \
        or (self.board[2] != ' ' and self.board[2] == self.board[4] and self.board[4] == self.board[6]) \
        or (self.board[2] != ' ' and self.board[2] == self.board[5] and self.board[5] == self.board[8]) \
        or (self.board[3] != ' ' and self.board[3] == self.board[4] and self.board[4] == self.board[5]) \
        or (self.board[6] != ' ' and self.board[6] == self.board[7] and self.board[7] == self.board[8]):
            self.winner = 'O' if self.current_shape == 'X' else 'X'
            return True
        elif self.is_board_full():
            self.winner = 'T'
            return True
        else:
            self.winner = None
            return False

    def play_loop(self):
        while True:
            try:
                self.output('*** OXO GAME SERVER STARTED ***')
                self.accept_clients()
                while True:
                    self.board = [' '] * BOARD_SIZE
                    self.current_player = randint(0,1)
                    self.current_shape = 'X' if randint(0,1) else 'O'
                    self.winner = None
                    self.send_message(self.current_player,'new game,' + self.current_shape)
                    self.send_message(self.current_player ^ 1,'new game,' + ('O' if self.current_shape == 'X' else 'X'))
                    while not self.is_game_finished():
                        self.send_message(self.current_player,'your move')
                        self.send_message(self.current_player ^ 1,'opponents move')
                        move_position = self.receive_message(self.current_player)
                        if not self.is_move_valid(move_position):
                            self.send_message(self.current_player,'invalid move')
                        else:
                            move_position = int(move_position)
                            self.board[move_position] = self.current_shape
                            valid_move_str = 'valid move,' + str(self.current_shape) + ',' + str(move_position)
                            self.send_message(self.current_player, valid_move_str)
                            self.send_message(self.current_player ^ 1, valid_move_str)
                            self.current_player = self.current_player ^ 1
                            self.current_shape = 'O' if self.current_shape == 'X' else 'X'
                    self.send_message(self.current_player,'game over,' + self.winner)
                    self.send_message(self.current_player ^ 1,'game over,' + self.winner)
                    self.send_message(self.current_player,'play again')
                    self.send_message(self.current_player ^ 1,'play again')
                    play_again_current = self.receive_message(self.current_player)[0].lower()
                    play_again_opponent = self.receive_message(self.current_player ^ 1)[0].lower()
                    if play_again_current != 'y' or play_again_opponent != 'y': 
                        self.send_message(self.current_player,'exit game')
                        self.send_message(self.current_player ^ 1,'exit game')
                        self.close_clients()
                        break
            except Exception as e:
                self.output('ERROR:' + str(e) + '\n\nGame Server is being restarted.\n')
                
def main():
    ogs = OXOGameServer()
    ogs.play_loop()

main()