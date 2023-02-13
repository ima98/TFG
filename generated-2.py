import pyforms
from   pyforms.basewidget import BaseWidget
from   pyforms.controls import ControlCheckBoxList,ControlMatplotlib,ControlCheckBox, ControlList,ControlTextArea,ControlLabel,ControlCodeEditor,ControlDockWidget,ControlEmptyWidget,ControlNumber,ControlCombo,ControlFile,ControlButton,ControlText
import OpenGL
import csv
import plotly.graph_objects as go
import pathlib
import os
import pandas as pd
import sys

from numpy import random

from sklearn.model_selection import train_test_split
from sklearn import neighbors, datasets, svm, linear_model
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report, hamming_loss,jaccard_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.base import BaseEstimator
import tensorflow as tf
from tensorflow import keras


import pandas as pd
from windowMain import *
import matplotlib.pyplot as plt
from scipy import rand

from keras.models import Sequential
from keras.layers import Dense, Dropout



from joblib import dump, load

import numpy as np


from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import errorManager

from scipy.io import arff


#https://pyforms.readthedocs.io/en/v3.0/api-documentation/basewidget/
from numpy import loadtxt
import tensorflow as tf
from keras.models import Sequential
dataL = arff.loadarff('C:/Users/imano/Desktop/tfg/app/iris.arff')
inputData = pd.DataFrame(dataL[0])
for dtype in inputData.dtypes.iteritems():
	if (dtype[1]=="O"):
		inputData[dtype[0]],_=pd.factorize(inputData[dtype[0]])
y = inputData.iloc[:,inputData.shape[1]-1]
X=inputData.iloc[:, 0:inputData.shape[1]-2]


inputs = keras.Input(shape=(inputData.shape[1],))

prim=tf.keras.layers.Dense(units= 12.0, activation= 'relu', use_bias= False, kernel_initializer= 'RandomNormal', bias_initializer= 'RandomNormal', kernel_regularizer= 'L1', bias_regularizer= 'L1', activity_regularizer= 'L1', kernel_constraint= 'MaxNorm', bias_constraint= 'MaxNorm')(inputs)
seg=tf.keras.layers.Dense(units= 12.0, activation= 'relu', use_bias= False, kernel_initializer= 'RandomNormal', bias_initializer= 'RandomNormal', kernel_regularizer= 'L1', bias_regularizer= 'L1', activity_regularizer= 'L1', kernel_constraint= 'MaxNorm', bias_constraint= 'MaxNorm')(prim)
ter = tf.keras.layers.Add()([prim, seg])
cuart=tf.keras.layers.Activation(activation= 'relu')(ter)

model=keras.Model(inputs,cuart)

#model.compile(optimizer='RMSprop', loss='BinaryCrossentropy', steps_per_execution=int(0), metrics=['Accuracy'])
#model.fit(X, y, epochs=int(20), batch_size=int(32), verbose='auto', validation_split=0.0)
model.summary()