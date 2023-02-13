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

    def __init__(self):
        """ inits the main window
        
        """
        super(mainWindow,self).__init__('Prueba grafica')

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.fileName=''

        self._output    =ControlTextArea()
        self._output.scrollbar=True
   

        self._saveOutputButton= ControlButton('Save as txt')
        self._saveOutputButton.value=self.__saveOutput

        self._classifierParams=ControlEmptyWidget()
 

        
        self._miniV=ControlDockWidget(side='top')
        variable=classifiersWindow(self)
        variable.parent=self
        self._miniV.value=variable

        self._ajustesEjecucion=ControlDockWidget()

        self._listaAnteriores=ControlDockWidget()
        self._listaAnteriores.value=historyWindow(self)

        self._nameSaveFile=ControlText('Save file name')

        self._modelBoolean=False

        self._formset=[
            {
            'Carga de datos':['_classifierParams'],
            
            'Clasificador':['_output',('_nameSaveFile','_botonCodigo')]
            }
            ]
        

        self._listaConfig=[]
        self._modelConfig=''

    def __saveOutput(self):
        """ guarda el output
        
        """
        f= open(self._nameSaveFile.value+".txt","w+")
        f.write(self._output.value)
        f.close()


    def _showClassifierParams(self, X):
        """ inicializa la ventaja de ajustes
        
        :param X: clasificador seleccionado
        """
        from os.path import exists
        import errorManager
        #exists(self.fileName) and
        if( self.fileName!=''):
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
