from classifiers.KNNsettings import *
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
            ('_loadFile','_loadModel'),
           '_listaClasi',
            '=','_ajustes'
            ]
        self._loadFile=ControlFile('Data file')
        self._loadFile.changed_event=self.__loadFile

        self._loadModel=ControlFile('Model file')
        self._loadModel.changed_event=self.__loadModel

        self._titulo=ControlLabel('Clasificadores')
        self._print=ControlLabel('printeos')

        ##config quitado de momento
        self._config=ControlFile(label="    Model")
        self._listaClasi = ControlCombo(label='     List')

        #for root, dirs, files in os.walk('./classifiers/'):
        #    for file in files:
        #        if file.endswith('.json'):
                    
        #            left_text = file.partition(".")[0]
        #            print(left_text)
        #            print(file.upper)
        #            self._listaClasi.add_item(left_text)
        import os

        root = "./classifiers/"
        for item in os.listdir(root):
            if os.path.isfile(os.path.join(root, item)):
                if item.endswith('.json'):
                    print(item)
                    left_text = item.partition(".")[0]
                    self._listaClasi.add_item(left_text)

    

        #self._listaClasi.add_item('KNN')
        #self._listaClasi.add_item('SVM')
        #self._listaClasi.add_item('MLP')
        self._listaClasi.add_item('KERAS')

        self._ajustes=ControlButton('Ajustar el clasificador')

        self._config.changed_event=self.__confiUpdate
        
        self._ajustes.value=self._showSettings


    def __loadModel(self):
        from joblib import load
        if(self._loadModel.value!=''):
            config=load(self._loadModel.value)
            print(config.listaConfig)
            self.parent._listaConfig=config.listaConfig
            print(config.model)
            self.parent._modelConfig=config.model
            self.parent._modelBoolean=True
            self._listaClasi.value=config.listaConfig[0]
            self._showSettings


        else:
            #aqui deberia haber un popup warning
            print('error')
        


    def __confiUpdate(self):
        left_text = self._config.value.partition("!")[0]
        self._listaClasi.value=left_text    

    def _showSettings(self):
        self.parent._showClassifierParams(self._listaClasi.value)

    def __loadFile(self):
        
        df = pd.read_csv(self._loadFile.value, header = 0)
        
        original_headers = list(df.columns.values)

        numeric_headers = list(df.columns.values)

        numpy_array = df.to_numpy

        shape=df.shape

        X= df._get_numeric_data().values.tolist()

        X=df.iloc[0,3].tolist()

        y, extra= pd.factorize(df[original_headers[shape[1]-1]].values)

        datos=[]
        clase=[]
        dat2=[]
        for i in range(shape[1]-2):
            dat2.append(df[original_headers[i]].values)
        #clase.append(df[original_headers[shape[1]-1]].values)
        clase, extra= pd.factorize(df[original_headers[shape[1]-1]].values)           
        datos.append(dat2)


        self.parent._output.value=[datos,clase]

        self.parent.fileName=self._loadFile.value