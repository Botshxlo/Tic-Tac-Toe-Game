# Botshelo Nokoane
# OXO Game GUI
# 17/05/2020

import os 
import sys
from time import *
from style import *
from sound import *
from GameClient import *
from PyQt5.QtGui import *  # imports pyqt modules
from PyQt5.QtCore import *  # imports pyqt modules
from PyQt5.QtWidgets import *  # imports pyqt modules
from PyQt5.QtMultimedia import *

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
        self.oIcon = QIcon(os.path.join("Icons", "nought.png"))
        self.xIcon = QIcon(os.path.join("Icons", "cross.png"))
        self.bIcon = QIcon(os.path.join("Icons", "blank.gif"))
        
        # answer of the user
        self.response_user = None
        
        # set window icon and color
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join("Icons", "game_icon.png")))
        self.setWindowIcon(icon)  # set window icon
        
        # set the sounds 
        """ part of the enhancements """
        self.sounds = feature_sound()
        """ @enhancements """
        
        # Create toggle button for change of theme
        """ part of the enhancements """
        self.toggle_button =  QPushButton("change theme")
        self.toggle_button.setFixedSize(120,30)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFont(QFont("Monospace",13,5))
        self.toggle_button.clicked.connect(self.change_theme)
        """ @enhancements """
        
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
        self.you = QLabel("You          ==>")
        self.you.setAlignment(Qt.AlignLeft)
        self.you.setFont(QFont("Arial",15,5))
        self.score_you = QLabel("0")
        self.score_you.setFont(QFont("Arial",15,5))
        self.opponent = QLabel("Opponent ==>")
        self.opponent.setAlignment(Qt.AlignLeft)
        self.opponent.setFont(QFont("Arial",15,5))
        self.score_opponent = QLabel("0")
        self.score_opponent.setFont(QFont("Arial",15,5))

        # create score board and players character layout
        self.player_grid = QGridLayout()
        self.player_grid.addWidget(self.my_shape_label,0,0)
        self.player_grid.addWidget(self.my_shape,0,1)
        self.player_grid.addWidget(self.score_label,1,0)
        self.player_grid.addWidget(self.you,2,0)
        self.player_grid.addWidget(self.score_you,2,1)
        self.player_grid.addWidget(self.opponent,3,0)
        self.player_grid.addWidget(self.score_opponent,3,1)
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
        self.grid_buttons.addWidget(self.toggle_button,0,2, alignment=Qt.AlignCenter)
        self.grid_buttons.addWidget(self.exit_button,0,4, alignment=Qt.AlignCenter)
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
        self.theme_counter = 0
        self.main_css = styler()
        self.changed_css0 = change_theme0()
        self.changed_css1 = change_theme1()
        self.main_layout_widget.setStyleSheet(self.main_css.toString())

        # connect buttons
        self.exit_button.clicked.connect(self.exit)

        # musk all buttons into one function
        self.allButtons = self.board_game_widget.findChildren(QToolButton)
        
        # connect signals to slots
        for self.button in self.allButtons:
            self.button.clicked.connect(self.button_clicked)
            
        # Disable the game board until the user has connect to the server
        self.board_game_widget.setEnabled(False)
            
        # set up loop thread    
        self.loop_thread = LoopThread()  # create thread
        self.loop_thread.msg_signal.connect(self.loop_thread_slot)  # connect signal to slot
        self.connect_btn.clicked.connect(self.connect_server) 
    
    """ part of enhancements """
    def change_theme(self):
        
        # if button is checked
        if self.toggle_button.isChecked():
            # change theme of the game and background color of the button
            
            if self.theme_counter%2 == 0:
                self.setPalette(QPalette(QColor("#996633")))  # brownish
                self.main_layout_widget.setStyleSheet(self.changed_css0.toString())  # brownish
                
            else:
                self.setPalette(QPalette(QColor("#990000")))  # redish
                self.main_layout_widget.setStyleSheet(self.changed_css1.toString())  # redish
            
            self.theme_counter += 1    
            
        else:
            # set the background color back to ''
            self.setPalette(QPalette(QColor("#498f7f")))
            self.main_layout_widget.setStyleSheet(self.main_css.toString())
    """ @enhancements """
            
    # Dialog window method
    """ part of the enhancements """
    def feature_dialog(self, condition=None, character=None):
        self.dialog_window = QDialog()  # Create dialog window
        self.dialog_window.setModal(True) 
        #self.dialog_window.setGeometry(200,200,200, 200)  # setting window geometries
        self.dialog_window.setWindowTitle("Feed")  # Set window title 
        self.dialog_window.setPalette(QPalette(QColor("#b3ffe6")))
        
        # vbox for the pixmap winner and play again label
        self.v_box = QVBoxLayout()
        
        # hbox for the buttons
        self.h_box = QHBoxLayout()
        
        # main vbox for the overall layout
        self.main_vbox = QVBoxLayout()

        # create pixmap label
        self.pixmap_label = QLabel("")
        
        # create widgets
        self.win_label = QLabel("")
        self.win_label.setFont(QFont("Arial",18,5))
        self.win_label.setAlignment(Qt.AlignCenter)
        
        self.play_label = QLabel("Play again?") 
        self.play_label.setFont(QFont("Arial",12,5))
        self.play_label.setAlignment(Qt.AlignCenter)
        
        # create buttons
        self.yes_button = QPushButton("Yes")
        self.yes_button.setObjectName("y")
        self.no_button = QPushButton("No")
        self.no_button.setObjectName("n")
        
        # connect signals to slots
        for button in [self.yes_button, self.no_button]:
            button.clicked.connect(self.response)
        
        # set the mixmap labels
        self.win_pixmap = QPixmap(os.path.join("Icons", "winIcon.png"))
        self.lose_pixmap = QPixmap(os.path.join("Icons", "loseIcon.png"))
        self.draw_pixmap = QPixmap(os.path.join("Icons", "drawIcon.png"))
        
        self.v_box.addWidget(self.pixmap_label, alignment=Qt.AlignCenter)
        self.v_box.addWidget(self.win_label)
        """ set vbox QWidget """
        self.vbox_widget = QWidget()
        self.vbox_widget.setLayout(self.v_box)
            
        self.h_box.addWidget(self.yes_button)
        self.h_box.addWidget(self.no_button)
        """ set hbox Widget """
        self.h_box_widget = QWidget()
        self.h_box_widget.setLayout(self.h_box)
            
        # set all widgets
        self.main_vbox.addWidget(self.vbox_widget)
        self.main_vbox.addWidget(self.play_label)
        self.main_vbox.addWidget(self.h_box_widget)
        
        # check for conditions
        if condition == "You Win!":
            self.pixmap_label.setPixmap(self.win_pixmap)
            self.win_label.setText("WINNER - " + character + "!")

        elif condition == "Its a Draw!":
            self.pixmap_label.setPixmap(self.draw_pixmap)
            self.win_label.setText("DRAW!")
            
        elif condition == "You lose!":
            self.pixmap_label.setPixmap(self.lose_pixmap)
            self.win_label.setText("LOSSER - " + character + "!")
            
        self.dialog_window.setLayout(self.main_vbox)
        self.dialog_window.show()
    """ @enhancements """    
    
    # loop thread method    
    def loop_thread_slot(self, txt):
        
        # check for messages from the server (new game,X or new game,O)
        if txt == "new game,X" or txt == "new game,O":
            
            # declare a new game
            self.reset_board()
            
            self.shape = txt[-1]  # player character
            self.server_messages.append(" \nnew game")  # append message to text edit
            
            # check for character
            if self.shape == "X":
                self.my_shape.setIcon(self.xIcon)   # set Icon
            elif self.shape == "O":
                self.my_shape.setIcon(self.oIcon)   # set Icon
                
            self.sounds["welcome"].play()  # play sound
                
        # chech for messages from the server (your or opponents move)
        if txt == "your move":
            self.server_messages.append(txt)
            
            # Enable the game board
            self.board_game_widget.setEnabled(True)
            
        elif txt =="opponents move":
            self.server_messages.append("opponents move")  # append message to text edit
            
            # Disable the game board         
            self.board_game_widget.setEnabled(False)
            
        # check for messages from the server (valid or invalid move)
        if txt[:10] == "valid move":
            self.shape_move = txt[11]  # character X or O                              
            self.number = txt[-1]  # object (button) number
            
            self.clicked_button = self.board_game_widget.findChild(QToolButton, str(self.number))  # locate the button that is clicked
            
            # check for character,set Icon and play sound
            if self.shape_move == "X":
                self.sounds["cross"].play()  
                
                self.clicked_button.setIcon(self.xIcon)  
                
            elif self.shape_move == "O":
                self.sounds["nought"].play()  
                
                self.clicked_button.setIcon(self.oIcon)  
            
        elif txt[:12] == "invalid move":
            self.server_messages.append("invalid move")  # append message to text edit
        
        # check for messages from the server (game over,O or game over,X and game over,T)    
        if txt == "game over,O" or txt == "game over,X":
            self.server_messages.append("game over")  # append message to text edit
            
            # check who won the game and display appropriate information (Dialog window)
            if self.shape == txt[-1]:
                self.condition = "You Win!"
                
                # show dialog window and play sound
                self.sounds["win"].play()
                
                self.server_messages.append(self.condition) # append message to text edit
                
                self.feature_dialog(condition=self.condition, character=self.shape)  # show dialog window
                
                # Update new score for the current winner
                self.new_score = int(self.score_you.text()) + 1
                self.score_you.setText(str(self.new_score))  # set new score

            else:    
                self.condition = "You lose!"
                
                # show dialog window and play sound
                self.server_messages.append(self.condition) # append message to text edit
                
                self.feature_dialog(condition=self.condition, character=self.shape)  # show dialog window
                
                # Update new score for the current loser
                self.new_score = int(self.score_opponent.text()) + 1
                self.score_opponent.setText(str(self.new_score))  # set new score
            
        elif txt == "game over,T":
            self.condition = "Its a Draw!"
            self.server_messages.append("game over\nits a Draw!") # append message to text edit
            
            self.feature_dialog(condition=self.condition, character="T") # display dialog window
        
        # check for messages from the server (game over)    
        if txt == "exit game":
            
            # check who ended the game
            if self.response_user == "n":
                self.server_messages.append("You left the game!") # append message to text edit
            else:
                self.server_messages.append("Opponent left the game!") # append message to text edit
                
            self.end_game() # decalre new game
                
    # reset board method
    def reset_board(self):
        # Enable game board and clear each button
        self.board_game_widget.setEnabled(True)
        
        for button in self.allButtons:
            button.setText("")
            button.setIcon(self.bIcon)
            button.setEnabled(True)
            
        self.my_shape.setIcon(self.bIcon)
    
    # new game method
    def end_game(self):
        self.reset_board() # reset the board
        
        self.feedback.setText("Disconnected")  # give user feedback
        
        self.server_messages.append("Click exit to exit the game")  # append message to text edit
        
        self.board_game_widget.setEnabled(False) # disable the board game
        
        # reset the score board
        self.score_you.setText("0")
        self.score_opponent.setText("0")
        
    # connect to the server method
    def connect_server(self):
        self.localhost = self.server_lineEdit.displayText().lower()  # get text from the Line Edit
        
        # check if input is valid
        if self.localhost in ["127.0.0.1","localhost"]:
            game.connect_to_server(self.localhost)  # connect to the server
            self.server_messages.insertPlainText("->Connected to the server!")  # give feedback to which server a player is connected to
            
            self.loop_thread.start()  # start the loop thread
            
            self.connect_btn.setEnabled(False)  # Disable the connect button for one user connection
            self.server_lineEdit.setEnabled(False)  # Disable the line edit for one user connection
        else:
            self.server_messages.append("->Error connecting to server!")    
            
        self.server_lineEdit.clear()  # clear the line edit
            
    # button clicked method        
    def button_clicked(self):
        
        self.sended = self.sender()
        self.button_number = self.sended.objectName() # get the object name
        game.send_message(str(self.button_number))  # send message to the server
    
    # response method        
    def response(self):
        
        self.res = self.sender() # retreives the clicked button
        self.res_answer = self.res.objectName() 
        
        if self.res_answer == "n":
            self.response_user = "n"
        else:
            self.response_user = "y"
                
        game.send_message(self.res_answer) # send messages to the server
            
        self.dialog_window.close()
            
    # exit method        
    def exit(self): 
        sys.exit()
        
app = QApplication(sys.argv)  # creates necessary app object
game = OXO_GAME()  # Instance of OXO_GUI class

def run_app():
    game.show()   # Show instance of OXO_GUI
    sys.exit(app.exec_())  # start executing main app event loop and return value to the exit system

if __name__ == "__main__":
    run_app()  # run the main app
