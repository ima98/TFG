from imports import *
import numpy as np
#from help import *
from numpy import loadtxt

class classifiersWindow(BaseWidget):
    def __init__(self, father):
        BaseWidget.__init__(self,'classifiersWindow')
        self.parent = father

        self.nextInputSize=0

        self.formset = [
            '_loadFile',('_loadModelString','_loadModelStringAction'),
           '_listaClasi',
            '=','_ajustes'
            ]
        self._loadFile=ControlFile('Data file')
        self._loadFile.changed_event=self.__loadFile



        #self._loadModel=ControlFile('Model file')
        #self._loadModel.changed_event=self.__loadModel
        #self._loadModel.hide()

        self._loadModelString=ControlText('Model string')
        self._loadModelString.hide()

        self._loadModelStringAction=ControlButton('Load String')
        self._loadModelStringAction.value=self.__loadStringModel
        self._loadModelStringAction.hide()

        self._titulo=ControlLabel('Clasificadores')
        self._print=ControlLabel('printeos')

        ##config quitado de momento
        #self._config=ControlFile(label="    Model")
        self._listaClasi = ControlCombo(label='     List')

        import os

        root = "./classifiers/"
        for item in os.listdir(root):
            if os.path.isfile(os.path.join(root, item)):
                if item.endswith('.json'):
                    left_text = item.partition(".")[0]
                    self._listaClasi.add_item(left_text)

    
        self._listaClasi.add_item('Sequential Model')
        self._listaClasi.add_item('Functional Model')

        self._listaClasi.changed_event=self.__deleteLoadedModel

        self._ajustes=ControlButton('Start')
        
        self._ajustes.value=self._showSettings

        
    def __deleteLoadedModel(self):
        self.parent._modelBoolean=False
        self._loadModelString.value=""


    def __loadStringModel(self):
        import json
        print(self._loadModelString.value)
        dict=json.loads(self._loadModelString.value)
        data=dict
        self.parent._modelConfig=data
        self.parent._modelBoolean=True

        try:
            
            X=data['type']
        except:
            
            tempDict=data[0]
            X=tempDict['type']
        self.parent._showClassifierParams(X) 

    def _showSettings(self):
        self.parent._showClassifierParams(self._listaClasi.value)

    def __loadFile(self):

        from os.path import exists
        import errorManager
        import json
        if(self._loadFile.value!=''):
            if(self._loadFile.value.endswith('.csv') or self._loadFile.value.endswith('.arff')):
                #if(exists(self._loadFile.value)):
                    self.parent.fileName=self._loadFile.value
                    #self._loadModel.show() 
                    self._loadModelString.show()
                    self._loadModelStringAction.show()
                #else:
                    #errorManager.error(self, "File doesn't exist", None)
            else:
                errorManager.error(self, "Error reading the model file", None)
                #self._loadModel.value=""
        else:
            self.parent.fileName=''
            errorManager.error(self, "File doesn't exist", None)
