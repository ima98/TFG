from asyncio.windows_events import NULL
from classifiers.KNNsettings import KNNsettings
from classifiers.SVMsettings import SVMsettings
from classifiers.MLPsettings import MLPsettings
from windowHistory import historyWindow
from windowClassifiers import classifiersWindow
from imports import *
import settings
from confapp import conf;
from windowSettings import *
conf+=settings
import matplotlib.pyplot as plt
from windowSettings import settingsWindow
from classifiers.sequentialModel import sequentialModel
from classifiers.sklearnBase import *


#constructor del basewidget menu principal
class mainWindow(BaseWidget):

    #globales

    def __init__(self):
        super(mainWindow,self).__init__('Prueba grafica')

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        self.actualCSV=0
        self.X=0
        self.y=0

        self.firstInputSize=0
        
        #self._loadFile     = ControlFile('Load data')
        #self._loadFile.changed_event=self._loadFile.value
        #self._figura=ControlMatplotlib()
      

        self._output    =ControlTextArea()
        #self._output.setReadOnly(True)
        self._output.scrollbar=True
        #self._output.value=self._loadFile.value

        self._code=ControlDockWidget()
        self._code.hide()
        self._botonCodigo= ControlButton('View code')
        self._botonCodigo.value=self._showCode

        self._classifierParams=ControlEmptyWidget()
        #self._classifierParams.hide()

        self._graph = ControlMatplotlib()

        
        self._miniV=ControlDockWidget(side='top')
        variable=classifiersWindow(self)
        variable.parent=self
        self._miniV.value=variable

        self._ajustesEjecucion=ControlDockWidget()
        ajustesVentana=settingsWindow()
        ajustesVentana.parent=self
        self._ajustesEjecucion.value=ajustesVentana


        self._ejecucionesAnteriores=ControlDockWidget()
        historial=historyWindow()
        historial.parent=self
        self._ejecucionesAnteriores.value=historial

        self._nameSaveFile=ControlText('Save file name')
        self._save=ControlButton('Save')
        self._save.value=self.__save
        self._modelBoolean=False

        self._formset=[
            {
            'Carga de datos':['_classifierParams'],
            
            'Clasificador':['_output',('_nameSaveFile','_save'),'_botonCodigo']
            }
            ]
        
    
        #configuración para guardar
        self._listaConfig=[]
        self._modelConfig=''

    def __save(self):
        m=modelConfig(self._listaConfig, self._modelConfig)
        t=self._nameSaveFile.value
        if self._nameSaveFile.value=='' :
            t='demo'
        
        from joblib import dump

        dump(m, t+'.joblib')

        

    
        

    def _showCode(self):

        prueba=ControlCodeEditor()
        prueba.value=self.actualCSV
        #self._output.value=self.actualCSVseRepiteNVeces (3, [a, b, c, e, f, a, b, f, h, g, h, f, a, i, c], S)
        self._code=prueba
        self._code.show()

    def _showClassifierParams(self, X):

        #if X=='KNN':
        #    prueba=sklearnBase(self, NULL,NULL, 'KNN')

        if X=='KERAS':
            prueba=sequentialModel(self,NULL,NULL)
        else:
            prueba=sklearnBase(self, NULL, NULL, X)
        #   
        self._classifierParams.value=prueba
        self._classifierParams.show()
        self._modelBoolean=False 
    
    
    def _updateConfig(self, c):
        self.variable._config.value=c

    def _do_something():
        "asasa"