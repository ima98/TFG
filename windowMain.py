from asyncio.windows_events import NULL
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
from classifiers.functionalModel import functionalModel
from classifiers.sklearnBase import *


#constructor del basewidget menu principal
class mainWindow(BaseWidget):

    #globales

    def __init__(self):
        super(mainWindow,self).__init__('Prueba grafica')

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)


        self.fileName=''

        self._output    =ControlTextArea()
        self._output.scrollbar=True
   

        self._code=ControlDockWidget()
        self._code.hide()
        self._botonCodigo= ControlButton('View code')
        self._botonCodigo.value=self._showCode

        self._classifierParams=ControlEmptyWidget()
 

        self._graph = ControlMatplotlib()

        
        self._miniV=ControlDockWidget(side='top')
        variable=classifiersWindow(self)
        variable.parent=self
        self._miniV.value=variable

        self._ajustesEjecucion=ControlDockWidget()
        #ajustesVentana=settingsWindow("SKLEARN")


        self._listaAnteriores=ControlDockWidget()
        self._listaAnteriores.value=historyWindow(self)

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
        if self._miniV.value._listaClasi.value=='Sequential Model':
            print("keras")
        else:
            print("sklearn")

    def _showCode(self):

        prueba=ControlCodeEditor()
        #prueba.value=self.actualCSV
        self._code=prueba
        self._code.show()

    def _showClassifierParams(self, X):
        from os.path import exists
        import errorManager
        if(exists(self.fileName) and self.fileName!=''):
            if X=='Sequential Model':
                prueba=sequentialModel(self)
                ajustesVentana=settingsWindow("KERAS")
                ajustesVentana.parent=self
                self._ajustesEjecucion.value=ajustesVentana

            elif X=='Functional Model':
                prueba=functionalModel(self)
                ajustesVentana=settingsWindow("KERAS")
                ajustesVentana.parent=self
                self._ajustesEjecucion.value=ajustesVentana

            else:
                prueba=sklearnBase(self, X)
                ajustesVentana=settingsWindow("SKLEARN")
                ajustesVentana.parent=self
                self._ajustesEjecucion.value=ajustesVentana

            self._classifierParams.value=prueba
            self._classifierParams.show()
        else:
            errorManager.error(self, "File doesn't exist", None)
            
    
    def _updateConfig(self, c):
        self.variable._config.value=c

    def _do_something():
        "asasa"