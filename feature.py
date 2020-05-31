# Botshelo Nokoane
# 2020/05/30
# enhancement

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from style import styler

class Dialog(QDialog):
    
    def __init__(self, parent=None, state=None):
        super(Dialog, self).__init__(parent)
        self.setModal(True)
        
        #
        feed_layout = QGridLayout(self)

        #
        pixmap_label = QLabel("")
        
        #
        win_label = QLabel("")
        win_label.setFont(QFont("Arial",18,5))
        win_label.setAlignment(Qt.AlignCenter)
        
        play_label = QLabel("Play again?")
        play_label.setAlignment(Qt.AlignCenter)
        
        #
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        
        #
        win_pixmap = QPixmap(os.path.join("Icons", "winIcon.png"))
        lose_pixmap = QPixmap(os.path.join("Icons", "loseIcon.png"))
        draw_pixmap = QPixmap(os.path.join("Icons", "drawIcon.png"))
        
        #
        if state == "You Win!":
            pixmap_label.setPixmap(win_pixmap)
            win_label.setText("You won!")
            
            feed_layout.addWidget(pixmap_label, 1,0)
            feed_layout.addWidget(win_label, 0, 1)
            feed_layout.addWidget(no_button, 2, 2)
            feed_layout.addWidget(yes_button, 2, 1)
            feed_layout.addWidget(play_label, 1, 1)
            

        elif state == "You lose!":
            pixmap_label.setPixmap(lose_pixmap)
            win_label.setText("You lost!")
            
            feed_layout.addWidget(pixmap_label, 1, 0)
            feed_layout.addWidget(win_label, 0, 1)
            feed_layout.addWidget(no_button, 2, 2)
            feed_layout.addWidget(yes_button, 2, 1)
            feed_layout.addWidget(play_label, 1, 1)
            

        else:
            pixmap_label.setPixmap(draw_pixmap)
            win_label.setText("It's a draw!")
            
            feed_layout.addWidget(pixmap_label, 1, 0)
            feed_layout.addWidget(win_label, 0, 1)
            feed_layout.addWidget(no_button, 2, 2)
            feed_layout.addWidget(yes_button, 2, 1)
            feed_layout.addWidget(play_label, 1, 1)
            
            
        yes_button.clicked.connect(self.hide)

        
        css = styler()
        feed_layout.setStyleSheet(css.toString())
        
        # set main layout
        #setLayout(feed_layout)
        #yes_button.clicked.connect(self.hide)
        
        # connect signals to slots
        #no_button.clicked(no)
        #yes_button.clicked(yes)
        
#game = GameClient()        

if __name__ == "__main__":
    app = QApplication([])
    dialog = Dialog(state="You win!")
    dialog.show()
    app.exec_()

        
        
        