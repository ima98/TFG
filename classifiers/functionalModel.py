from imports import *
from classifiers.layers.layer import layer
from classifiers.layers.layerFunctional import layerFunctional
from numpy import loadtxt
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
import tensorflow as tf
from tensorflow import keras

from io import StringIO 
import sys


#https://stackoverflow.com/questions/52591862/how-can-i-save-an-object-containing-keras-models
#https://stackoverflow.com/questions/39369671/can-i-store-a-file-hdf5-file-in-another-file-with-serialization/39386944#39386944
class functionalModel(BaseWidget):
    def __init__(self, father):
        self.parent=father
        
        self.model=Sequential()
        
        BaseWidget.__init__(self,'Functional mode')
        
        self.layers=[]
        self.layerNames=[]
        
        self._layerType=ControlCombo('layer types')
        root = "./classifiers/layers"
        for item in os.listdir(root):
            if os.path.isfile(os.path.join(root, item)):
                if item.endswith('.json'):
                    print(item)
                    left_text = item.partition(".")[0]
                    self._layerType.add_item(left_text)
        self._layerType.add_item('Input from layers')
        
        self._layerCombo=ControlCombo('layers')
 
        self._addLayer=ControlButton('Config Layer')
        self._addLayer.value=self.__addLayer
        self._deleteLayer=ControlButton('Delete layer')
        self._deleteLayer.value=self.__deleteLayer
        self._editLayer=ControlButton('Edit layer')
        self._editLayer.value=self.__editLayer

        
        
        self._layer=ControlEmptyWidget()

        self._layerEdit=ControlEmptyWidget()
        
        self._execute=ControlButton('Execute')
        self._execute.value=self.__execute
        
        
        self._generatePy=ControlButton('Generate Py')
        self._generatePy.value=self.__generatePy

        self._saveModel=ControlButton('Save model')
        self._saveModel.value=self.__saveModel

        self.formset=['_layerType','_addLayer', '_layer','_layerCombo','_layerEdit',('_deleteLayer', '_editLayer'),('_generatePy', '_saveModel'),'_execute']
        

        if self.parent._modelConfig is not None and self.parent._modelBoolean:
            self.__loadSettings(self.parent._modelConfig) 
    
    def __addLayer(self):
        self._layerEdit.hide()
        self._layer.show()
        prueba=layerFunctional(self._layerType.value, self)
        
        prueba.parent=self
        self._layer.value=prueba
        
        
                
    def __addLayerToModel(self, l):
        self.layers.append(l)
        self._layerCombo.add_item(l['_name'],l)
        self._layer.hide()
        print(self.layers)


    def __deleteLayer(self):
        delete=self._layerCombo.value
        self.layers.remove(delete)
        self._layerCombo.clear()
        for x in self.layers:
            self._layerCombo.add_item(x)
            

    def __editLayerOrder(self):
        self.windowOrder.show()
        self.windowOrder.updateLista(self.layers)

    def _WindowLayerOrder__setLayerLista(self, lista):
        self.layers=lista
        self.__generateComboFromList()
        

    def _layer__addEditedLayer(self, dic):
        for item in self.layers:
            if item['self._name']==dic['self._name']:
                self.layers[self.layers.index(item)]=dic
        
        self._layerEdit.hide()
        
        
        self.__generateComboFromList()

        

    def __editLayer(self):
        self._layer.hide()
        self._layerEdit.show()
        prueba=layerFunctional(self._layerType.value, self, self._layerCombo.value)
        prueba.parent=self
        self._layerEdit.value=prueba

    
    def __generateComboFromList(self):
        self._layerCombo.clear()
        for layerDic in self.layers:
            #print(layerDic)
            #dic['self._name'],dic
            self._layerCombo.add_item(layerDic['self._name'], layerDic)
        #print(self._layerCombo.items)
        
    def __generatePy(self):
        import fileGenerator
        toAdd=""
        stringList=[]
        for layerDic in self.layers:
            print(layerDic)
            if(layerDic['type']=='Input from layers'):
                m="layerDic['self._name'] = layers.add(layerDic['input'])"
            else:
                cons=layerDic['constructor']
                tempName=str(layerDic['self._name'])
                tempInput=layerDic['input']
                if tempInput==None:
                    m=str(tempName)+'='+cons+'(inputs)'
                else:
                    m=str(tempName)+'='+cons+'('+tempInput+')'
            print(m)

        listaMetrics=self.__getListaMetrics()
        compileList=[self.parent._ajustesEjecucion.value._seq_optimizers.value, self.parent._ajustesEjecucion.value._seq_loss.value, int(self.parent._ajustesEjecucion.value._seq_compile_steps_per_execution.value),
            listaMetrics]

        fitList=[int(self.parent._ajustesEjecucion.value._fit_epochs.value), int(self.parent._ajustesEjecucion.value._fit_batch_size.value), self.parent._ajustesEjecucion.value._fit_verbose.value, 
            self.parent._ajustesEjecucion.value._fit_validation_split.value]

        #fileGenerator.fileGeneratorSequentialModel(stringList, self.parent.fileName, compileList, fitList)


    def __getListaMetrics(self):
        listaMetrics=self.parent._ajustesEjecucion.value._seq_metrics.items
        l2=[]
        for x in listaMetrics:
                if x[1]==True:
                    l2.append(x[0])
        return l2

    def __saveModel(self):
        model = Sequential()

        for layerDic in self.layers:
            print("keys de las capas en el modelo \n")
            print(layerDic.keys())
            cons=layerDic['constructor']
            m='layerTemp='+cons
            exec(m)
            exec("model.add(layerTemp)")
        model.save('my_model.h5')

    def __loadSettings(self, lista):
        lista.pop(0)
        self.layers=lista
        for x in lista:
            self.layerNames.append(x['self._name'])
        self.__generateComboFromList()


    def __execute(self):

        import errorManager
        try:
            import helper
            (X,y,dataset)=helper.getDataSet(self.parent.fileName)

   
        except Exception as e: 
            errorManager.error(self, "Error loading the csv", e)
            return


        sys.stdout = buffer = StringIO()

        from sklearn.model_selection import train_test_split
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=self.parent._ajustesEjecucion.value._sk_train_test_split_test_size.value,
        random_state=int(self.parent._ajustesEjecucion.value._sk_random_state.value), shuffle=self.parent._ajustesEjecucion.value._sk_shuffle.value)

        
        inputs = keras.Input(shape=(dataset.shape[1],))

        tempName=''

        lastLayer=''

        for layerDic in self.layers:
            if(layerDic['type']=='Input from layers'):
                lisL=str(str(layerDic['list']))
                lisL=lisL.replace("'","")
                m=layerDic['self._name']+" = tf.keras.layers.Add()("+lisL+")"
                print(m)
                print(layerDic['list'])
            else:
                cons=layerDic['constructor']
                tempName=str(layerDic['self._name'])
                tempInput=layerDic['input']
                if tempInput==None:
                    m=str(tempName)+'='+cons+'(inputs)'
                else:
                    m=str(tempName)+'='+cons+'('+tempInput+')'
            exec(m)

        exec('self.model=keras.Model(inputs,'+tempName+')')
        

        import errorManager
        try:
            listaMetrics=self.__getListaMetrics()

            self.model.compile(optimizer=self.parent._ajustesEjecucion.value._seq_optimizers.value, loss=self.parent._ajustesEjecucion.value._seq_loss.value, steps_per_execution=int(self.parent._ajustesEjecucion.value._seq_compile_steps_per_execution.value),
            metrics=listaMetrics)
        except Exception as e:
            errorManager.error(self, "Error during model compile", e)



        #FIT
        try:
            self.model.fit(X_train,y_train, epochs=int(self.parent._ajustesEjecucion.value._fit_epochs.value), batch_size=int(self.parent._ajustesEjecucion.value._fit_batch_size.value), verbose=self.parent._ajustesEjecucion.value._fit_verbose.value, 
            validation_split=self.parent._ajustesEjecucion.value._fit_validation_split.value)

        except Exception as e:
            errorManager.error(self, "Error during model fit", e)

        

        print(self.parent._ajustesEjecucion.value._fit_epochs.value)

      
        
        
        try:
             _, accuracy = self.model.evaluate(X_test, y_test, y)
             print('Accuracy: %.2f' % (accuracy*100))

        except Exception as e:
            errorManager.error(self, "Error during model evaluation", e)   

        self.model.summary()

        result=buffer.getvalue()

        self.parent._output.value=result
        