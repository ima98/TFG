import pyforms
from   pyforms.controls import ControlText, ControlMdiArea
from   pyforms.controls import ControlButton

from   pyforms.basewidget import BaseWidget

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap

from imports import *

class SimpleExample1(BaseWidget):

    def __init__(self):
        super(SimpleExample1,self).__init__('Simple example 1')

        #Definition of the forms fields
        self._firstname     = ControlText('First name', 'Default value')
        self._middlename    = ControlText('Middle name')
        self._lastname      = ControlText('Lastname name')
        self._fullname      = ControlText('Full name')
        

        self.setAcceptDrops(True)
        
        self._controlList=ControlList('lista')

        for l in ['A', 'B', 'C', 'D']:
            self._controlList.__add__(l)


        self._controlList.readonly=True
        self._controlList.set_sorting_enabled=True


        self._controlList.add_popup_menu_option('option 1', function_action=self.function1)

        self._boton=ControlButton('ventana nueva')
        self._boton.value=self.nuevaPes
        
        self.ventana =Window()
        self.ventana.hide()

    def dragEnterEvent(self, e):
        e.accept()

    def function1(self):
        print(1)
    
    def nuevaPes(self):
        self.ventana.show()
        
class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.blayout = QHBoxLayout()
        for l in ['A', 'B', 'C', 'D']:
            btn = QPushButton(l)
            self.blayout.addWidget(btn)

        self.setLayout(self.blayout)

#Execute the application
if __name__ == "__main__":   pyforms.start_app( SimpleExample1 )