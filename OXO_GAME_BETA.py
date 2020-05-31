# Botshelo Nokoane
# OXO Game GUI
# 17/05/2020

import sys
from PyQt5.QtWidgets import *  # imports pyqt modules
from PyQt5.QtCore import *  # imports pyqt modules
from PyQt5.QtGui import *  # imports pyqt modules
from style import styler
from GameClient import *
import time

class LoopThread(QThread):
    
    msg_signal = pyqtSignal(str)  # create signal
    
    def __init__(self):
        QThread.__init__(self)
        
    def run(self):
        while True:
            msg = game.receive_message()  # recieve message from the server
            if len(msg):
                self.msg_signal.emit(msg)     # emit message

class OXO_GAME(QWidget, GameClient):  # Stock inherits from the Qwidget
    
    def __init__(self, parent=None):  # parent defines parent widget
        QWidget.__init__(self, parent)  # Super class instuctor
        GameClient.__init__(self)  # super class instructor
        
        self.setWindowTitle("O X O Client")  # Set window title
        self.setGeometry(390, 90, 610, 500)  # setting window geometries
        self.setPalette(QPalette(QColor("#498f7f")))

        # set the X,O and blank Icon
        self.oIcon = QIcon("nought.gif")
        self.xIcon = QIcon("cross.gif")
        self.bIcon = QIcon("blank.gif")
        
        # set the shape of each player and object name for each name
        self.dic_number = {"number":0}

        # set window icon and color
        icon = QIcon()
        icon.addPixmap(QPixmap("game_icon.png"))
        self.setWindowIcon(icon)  # set window icon

        # create header
        self.header = QLabel("TenElevenGames OXO")
        self.header.setFont(QFont("Arial",22,5))
        self.header.setAlignment(Qt.AlignCenter)

        # create server button label
        self.server_label = QLabel("server:")
        self.server_label.setFont(QFont("Monospace",13,5))
        self.server_lineEdit = QLineEdit()
        self.server_lineEdit.setFont(QFont("Monospace",13,5))
        self.server_lineEdit.setPlaceholderText("enter server")
        self.connect_btn = QPushButton("connect")
        self.connect_btn.setFont(QFont("Monospace",13,5))

        # create game and message headers
        self.the_game_label = QLabel("-----The Game-----")
        self.the_game_label.setAlignment(Qt.AlignCenter)
        self.the_game_label.setFont(QFont("Monospace",13,5))
        self.messages_label = QLabel("-----Messages from the server-----")
        self.messages_label.setAlignment(Qt.AlignCenter)
        self.messages_label.setFont(QFont("Monospace",13,5))
        self.header_hbox = QHBoxLayout()
        self.header_hbox.addWidget(self.the_game_label)
        self.header_hbox.addWidget(self.messages_label)
        """ header hbox widget """
        self.header_hbox_widget = QWidget()
        self.header_hbox_widget.setLayout(self.header_hbox)

        # insert server label and buttons
        self.horizontal = QGridLayout()
        self.horizontal.addWidget(self.header,0,1,1,1)
        self.horizontal.addWidget(self.server_label,1,0)
        self.horizontal.addWidget(self.server_lineEdit,1,1)
        self.horizontal.addWidget(self.connect_btn,1,2)
        self.horizontal.setAlignment(Qt.AlignTop)  # align the grid layout at the top
        """ Horizontal QWidget  """
        self.horizontal_widget = QWidget()
        self.horizontal_widget.setLayout(self.horizontal)


        # set up widget for Text message
        self.server_messages = QTextEdit()
        self.server_messages.setFont(QFont("Arial",13,5))
        self.server_messages.setStyleSheet("background-color: white")
        self.server_messages.setReadOnly(True)

        # players character and score board display
        self.my_shape = QPushButton()
        self.my_shape.setText("")
        self.my_shape.setEnabled(True)
        self.my_shape.setFixedSize(50,50)
        self.my_shape.setIconSize(QSize(50,50))
        self.my_shape.setStyleSheet("background-color: white")

        self.my_shape_label = QLabel("My shape")
        self.my_shape_label.setEnabled(False)
        self.my_shape_label.setFont(QFont("Arial",15,5))
        self.score_label = QLabel("Score:")
        self.score_label.setFont(QFont("Arial",15,5))
        self.character_x = QLabel("Player X==>")
        self.character_x.setAlignment(Qt.AlignCenter)
        self.character_x.setFont(QFont("Arial",15,5))
        self.score_x = QLabel("0")
        self.score_x.setFont(QFont("Arial",15,5))
        self.character_o = QLabel("Player O==>")
        self.character_o.setAlignment(Qt.AlignCenter)
        self.character_o.setFont(QFont("Arial",15,5))
        self.score_o = QLabel("0")
        self.score_o.setFont(QFont("Arial",15,5))

        # create score board and players character layout
        self.player_grid = QGridLayout()
        self.player_grid.addWidget(self.my_shape_label,0,0)
        self.player_grid.addWidget(self.my_shape,0,1)
        self.player_grid.addWidget(self.score_label,1,0)
        self.player_grid.addWidget(self.character_o,2,0)
        self.player_grid.addWidget(self.score_o,2,1)
        self.player_grid.addWidget(self.character_x,3,0)
        self.player_grid.addWidget(self.score_x,3,1)
        """ player_grid widget """
        self.player_grid_widget = QWidget()
        self.player_grid_widget.setLayout(self.player_grid)

        # vertical box for server messages and player_grid
        self.vertical = QVBoxLayout()
        self.vertical.addWidget(self.server_messages)
        self.vertical.addWidget(self.player_grid_widget)
        """ vertcial widget """
        self.vertical_widget = QWidget()
        self.vertical_widget.setLayout(self.vertical)

        # create Gird board game for buttons
        self.board_game = QGridLayout()
        self.board_game.setContentsMargins(0,0,0,0)
        self.board_game.setSpacing(0)
        self.object_name, self.row = 0, 0  # set the row and object name variable

        while self.row <= 2:  # while loop for the rows
            for self.column in range(3):  # for loop for the columns
                self.button = QToolButton()
                self.button.setText("")
                self.button.setFixedSize(100,100)
                self.button.setObjectName(str(self.object_name))
                self.button.setStyleSheet("background: white")
                self.button.setIconSize(QSize(100, 100))
                self.board_game.addWidget(self.button, self.row, self.column, 1, 1)
                self.object_name += 1  # increment each object name
            self.row += 1
        """ Board game QWidget """
        self.board_game_widget = QWidget()
        self.board_game_widget.setLayout(self.board_game)

        # create feedback Label and exit button
        self.feedback = QLabel()
        self.feedback.setFont(QFont("Monospace",13,5))
        self.exit_button = QPushButton("exit")
        self.exit_button.setFixedSize(90,20)
        self.exit_button.setFont(QFont("Monospace",13,5))

        self.grid_buttons = QGridLayout()
        self.grid_buttons.addWidget(self.feedback,0,3)
        self.grid_buttons.addWidget(self.exit_button,0,4)
        """ grid_buttons QWidget """
        self.grid_buttons_widget = QWidget()
        self.grid_buttons_widget.setLayout(self.grid_buttons)

        # HBox for the board game and text messages
        self.board_message = QHBoxLayout()
        self.board_message.addWidget(self.board_game_widget)
        self.board_message.setSpacing(7)
        self.board_message.addWidget(self.vertical_widget)  # Add a QWidget containing the self.log and a players information
        """ baord_message QWidget """
        self.board_message_widget = QWidget()
        self.board_message_widget.setLayout(self.board_message)  #

        # Insert widgets into vertical box
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.horizontal_widget)
        self.main_layout.addWidget(self.header_hbox_widget)
        self.main_layout.addWidget(self.board_message_widget)
        self.main_layout.addWidget(self.grid_buttons_widget)
        self.main_layout_widget = QWidget()
        self.main_layout_widget.setLayout(self.main_layout)

        # set main UI Layout
        self.ui = QVBoxLayout()
        self.ui.addWidget(self.main_layout_widget)
        self.setLayout(self.ui)

        # set the StyleSheet for the main layout
        css = styler()
        self.main_layout_widget.setStyleSheet(css.toString())

        # connect buttons
        self.exit_button.clicked.connect(self.exit)

        # musk all buttons into one function
        self.allButtons = self.board_game_widget.findChildren(QToolButton)
        self.availableButtons = self.allButtons[:]
        for self.button in self.allButtons:
            self.button.clicked.connect(self.button_add_icon)
            
        # set up loop thread    
        self.loop_thread = LoopThread()  # create thread
        self.loop_thread.msg_signal.connect(self.loop_thread_slot)  # connect signal to slot
        self.connect_btn.clicked.connect(self.connect_server)  

    def loop_thread_slot(self, txt):
        
        # check for messages from the server (new game,X or new game,O)
        if txt == "new game,X" or txt == "new game,O":
            self.shape = txt[-1]  # player character
            self.server_messages.append("new game")  # add text to server messages box
            
            # check for character
            if self.shape == "X":
                self.my_shape.setIcon(self.xIcon)
            elif self.shape == "O":
                self.my_shape.setIcon(self.oIcon)    
        
        # chech for messages from the server (your or opponents move)
        if txt == "your move":
            self.server_messages.append(txt)
            
            # Enable the game board
            self.board_game_widget.setEnabled(True)
            
        elif txt =="opponents move":
            self.server_messages.append("opponents move")         
            
            # Disable the game board         
            self.board_game_widget.setEnabled(False)
            
        # check for messages from the server (valid or invalid move)
        if txt[:10] == "valid move":
            self.shape_move = txt[11]  # character X or O                              
            self.number = txt[-1]  # object (button) number
            self.clicked_button = self.board_game_widget.findChild(QToolButton, str(self.number))  # locate the button that is clicked
            
            # check for character and set Icon
            if self.shape_move == "X":
                self.clicked_button.setIcon(self.xIcon)

            elif self.shape_move == "O":
                self.clicked_button.setIcon(self.oIcon)
                
            self.availableButtons.remove(self.clicked_button)  # remove the button is clicked    
            
        elif txt[:12] == "invalid move":
            self.server_messages.append("invalid move")
        
        # check for messages from the server (game over,O or game over,X and game over,T)    
        if txt == "game over,O" or txt == "game over,X":
            self.server_messages.append("game over")
            
            # check who won the game
            if self.shape == txt[-1] and self.shape == "X":
                self.server_messages.append("You win!")
                
                # update new score
                self.old_score = self.score_x.text()
                self.new_score = int(self.old_score) + 1 
                self.score_x.setText(str(self.new_score))
                
            elif self.shape == txt[-1] and self.shape == "O":
                self.server_messages.append("You win!")
                
                # update new score
                self.old_score = self.score_o.text()
                self.new_score = int(self.old_score) + 1 
                self.score_o.setText(str(self.new_score))
                
            else:    
                self.server_messages.append("You lose!")    
            
        elif txt == "game over,T":
            self.server_messages.append("game over\nits a Draw!")  
                
                
    # Method to connect to the server
    def connect_server(self):
        self.localhost = self.server_lineEdit.displayText().lower()  # get text from the Line Edit
        
        # check if input is valid
        if self.localhost in ["127.0.0.1","localhost"]:
            game.connect_to_server(self.localhost)  # connect to the server
            self.feedback.setText("connected to " + self.localhost)  # give feedback to which server a player is connected to
            
            self.loop_thread.start()  # start the loop thread
            
            self.connect_btn.setEnabled(False)  # Disable the connect button for one user connection
            self.server_lineEdit.setEnabled(False)  # Disable the line edit for one user connection
        else:
            self.feedback.setText("Enter a valid server url!")    
            
    def button_add_icon(self):  # buttons function
        
        self.sended = self.sender()
        self.button_number = self.sended.objectName() # get the object name
        game.send_message(str(self.button_number))  # send the message to the server
        
    def exit(self):  # exit button function
        sys.exit()

app = QApplication(sys.argv)  # creates necessary app object
game = OXO_GAME()  # Instance of OXO_GUI class

def run_app():
    game.show()   # Show instance of OXO_GUI
    sys.exit(app.exec_())  # start executing main app event loop and return value to the exit system

if __name__ == "__main__":
    run_app()  # run the main app
