from imports import *
import json

import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras import layers

from keras.models import Sequential
from keras.layers import Dense, Dropout

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap

class orderLayers(BaseWidget):
    def __init__(self, *args): 
        BaseWidget.__init__(self, 'order layers')

        layVer = QVBoxLayout()
        self.comBox = QComboBox()
        self.comBox.addItems(["One", "Two", "Three"])
        self.comBox.activated.connect(lambda x: self.onComBox(x))
        layVer.addWidget(self.comBox)
        

        layHor = QHBoxLayout()
        self.cheBox1 = QCheckBox("A")
        layHor.addWidget(self.cheBox1)
        layVer.addLayout(layHor)

        self.setLayout(layVer)

        #self.setLayout(self.blayout)

        #w = Window()
        #w.show()