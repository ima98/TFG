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
from sklearn import neighbors, datasets, svm
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
from globals import *
from scipy import rand





from joblib import dump, load

import numpy as np


from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import errorManager


#https://pyforms.readthedocs.io/en/v3.0/api-documentation/basewidget/