# Botshelo Nokoane
# 2020/06/01    
# enhancement "sounds"

import os
from PyQt5.QtMultimedia import *


def feature_sound():
    # set the sounds 
    """ part of the enhancement """
    sounds = dict(
        nought=QSound(os.path.join("Sounds", "nought.wav")),
        cross=QSound(os.path.join("Sounds", "cross.wav")),
        win=QSound(os.path.join("Sounds", "win.wav")),
        lose=QSound(os.path.join("Sounds", "lose.wav")),
        welcome=QSound(os.path.join("Sounds", "welcome.wav")),
        error=QSound(os.path.join("Sounds", "error.wav")),
        connected=QSound(os.path.join("Sounds", "connected.wav")),
    )
    
    return sounds