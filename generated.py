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
from scipy.io import arff
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


import pandas as pd
from windowMain import *
import matplotlib.pyplot as plt
from scipy import rand





from joblib import dump, load

import numpy as np


from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import errorManager


#https://pyforms.readthedocs.io/en/v3.0/api-documentation/basewidget/
#LOADING DATA
from pandas import read_csv 


data = arff.loadarff('C:/Users/imano/Desktop/tfg/app/iris.arff')
#inputData = read_csv('C:/Users/imano/Desktop/tfg/app/iris.csv', delimiter=',', header=1) 
inputData = pd.DataFrame(data[0])


y = inputData.iloc[:,inputData.shape[1]-1] 
X=inputData.iloc[:, 0:inputData.shape[1]-2] 

for dtype in inputData.dtypes.iteritems():
                    if (dtype[1]=='O'):
                        inputData[dtype[0]],_=pd.factorize(inputData[dtype[0]])

y = inputData.iloc[:,inputData.shape[1]-1] 
X=inputData.iloc[:, 0:inputData.shape[1]-2] 


#DATA SPLIT 
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25, random_state=int(0), shuffle=False)
modelo=sklearn.neighbors.KNeighborsClassifier(n_neighbors= 7, weights= 'uniform', algorithm= 'auto', leaf_size= 32, p= 4, metric= 'cityblock', n_jobs= 1)
modelo.fit(X_train,y_train)

print(modelo.predict(X_test))
