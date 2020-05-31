# DO NOT MODIFY THIS FILE

import sys
from datetime import *
from socket import *
from GameIni import *

# Basic networking and output(screen and logfile) functionality

class GameServer:
    
    def __init__(self):
        self.log_file = open(GAME_NAME + 'GameServer.log','w')
        self.log_file.close()
        self.output(GAME_NAME + ' Game Server Started: ' + str(datetime.now()))
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', PORT))
        self.socket.listen(2)
    
    def accept_clients(self):
        self.clients = []
        self.output('Waiting for client connections.')
        self.clients.append(self.socket.accept())
        self.output('Connected Client 0: ' + str(self.clients[0][1]))
        self.clients.append(self.socket.accept())
        self.output('Connected Client 1: ' + str(self.clients[1][1]))
    
    def send_message(self,i,msg):
        self.clients[i][0].send(BUFFER_STR.format(msg).encode())
        self.output('Sent Message Client ' + str(i) + ': ' + msg)

    def receive_message(self,i):
        msg = self.clients[i][0].recv(BUFFER_SIZE).decode().strip()
        self.output('Received Message Client ' + str(i) + ': ' + msg)
        return msg
    
    def close_clients(self):
        self.clients[0][0].close()
        self.output('Closed Client 0: ' + str(self.clients[0][1]))
        self.clients[1][0].close()
        self.output('Closed Client 1: ' + str(self.clients[1][1]))
        self.clients = []
        
    def output(self,msg):
        print(msg + '\n')
        sys.stdout.flush()
        self.log_file = open(GAME_NAME + 'GameServer.log','a')
        self.log_file.write(msg + '\n')
        self.log_file.close()
        
    def __del__(self):
        self.socket.close()
        self.output(GAME_NAME + ' Game Server Ended: ' + str(datetime.now()))

