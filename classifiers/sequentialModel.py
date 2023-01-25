from imports import *
from classifiers.layers.layer import layer
from numpy import loadtxt
import tensorflow as tf
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense
#from tensorflow.keras.optimizers import Adam
#from tensorflow.keras.losses import BinaryCrossentropy
#from tensorflow.keras.metrics import BinaryAccuracy, FalseNegatives

from classifiers.layers.orderLayers import *



from io import StringIO 
import sys




#https://stackoverflow.com/questions/52591862/how-can-i-save-an-object-containing-keras-models
#https://stackoverflow.com/questions/39369671/can-i-store-a-file-hdf5-file-in-another-file-with-serialization/39386944#39386944
class sequentialModel(BaseWidget):
    def __init__(self, father):
        self.parent=father
        
        self.model=Sequential()
        
        BaseWidget.__init__(self,'Sequential mode')
        
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
        

        self._editLayerOrder=ControlButton('Edit order')
        self._editLayerOrder.value=self.__editLayerOrder
        self.windowOrder=WindowLayerOrder(self)
        self.windowOrder.father=self
        self.windowOrder.hide()
        
        self._generatePy=ControlButton('Generate Py')
        self._generatePy.value=self.__generatePy

        self._saveModel=ControlButton('Save model')
        self._saveModel.value=self.__saveModel

        self.formset=['_layerType','_addLayer', '_layer','_layerCombo','_layerEdit',('_deleteLayer', '_editLayer', '_editLayerOrder'),('_generatePy', '_saveModel'),'_execute']
        

        if self.parent._modelConfig is not None and self.parent._modelBoolean:
            self.__loadSettings(self.parent._modelConfig)

        
        
    
    def __addLayer(self):
        self._layerEdit.hide()
        self._layer.show()
        prueba=layer(self._layerType.value, self)
        
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
        prueba=layer(self._layerType.value, self, self._layerCombo.value)
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
                cons=layerDic['constructor']
                m='layerTemp='+cons
                stringList.append(m)

        listaMetrics=self.__getListaMetrics()
        compileList=[self.parent._ajustesEjecucion.value._seq_optimizers.value, self.parent._ajustesEjecucion.value._seq_loss.value, int(self.parent._ajustesEjecucion.value._seq_compile_steps_per_execution.value),
            listaMetrics]

        fitList=[int(self.parent._ajustesEjecucion.value._fit_epochs.value), int(self.parent._ajustesEjecucion.value._fit_batch_size.value), self.parent._ajustesEjecucion.value._fit_verbose.value, 
            self.parent._ajustesEjecucion.value._fit_validation_split.value]

        fileGenerator.fileGeneratorSequentialModel(stringList, self.parent.fileName, compileList, fitList)


    def __getListaMetrics(self):
        listaMetrics=self.parent._ajustesEjecucion.value._seq_metrics.items
        l2=[]
        for x in listaMetrics:
                if x[1]==True:
                    l2.append(x[0])
        return l2

    def __saveModel(self):
        temp=self.layers
        typeTemp=[("type", "Sequential Model")]
        head=dict(typeTemp)
        temp.insert(0, head)
        data= json.dumps(temp, indent=2)
        with open("sample.json", "w") as outfile:
            outfile.write(data)

    def __loadSettings(self, lista):
        lista.pop(0)
        self.layers=lista
        for x in lista:
            self.layerNames.append(x['self._name'])
        self.__generateComboFromList()


    def __execute(self):

        dataset = loadtxt(self.parent.fileName, delimiter=',')
        
        # split into input (X) and output (y) variables
        X = dataset[:,0:dataset.shape[1]-1]
        y = dataset[:,dataset.shape[1]-1]



        from sklearn.model_selection import train_test_split
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=self.parent._ajustesEjecucion.value._sk_train_test_split_test_size.value,
        random_state=int(self.parent._ajustesEjecucion.value._sk_random_state.value), shuffle=self.parent._ajustesEjecucion.value._sk_shuffle.value)

        
        model = Sequential()

        for layerDic in self.layers:
            cons=layerDic['constructor']
            m='layerTemp='+cons
            exec(m)
            exec("model.add(layerTemp)")



        import datetime
        temp=self.layers
        typeTemp=[("type", "Sequential Model")]
        head=dict(typeTemp)
        temp.insert(0, head)
        now = datetime.datetime.now()
        self.parent._listaAnteriores.value.listaHistorial.append((("Sequential"+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)), temp))
        self.parent._listaAnteriores.value.__update()


        
        import errorManager
        try:
            listaMetrics=self.__getListaMetrics()

            model.compile(optimizer=self.parent._ajustesEjecucion.value._seq_optimizers.value, loss=self.parent._ajustesEjecucion.value._seq_loss.value, steps_per_execution=int(self.parent._ajustesEjecucion.value._seq_compile_steps_per_execution.value),
            metrics=listaMetrics)
        except Exception as e:
            errorManager.error(self, "Error during model compile", e)



        #FIT
        try:
            model.fit(X_train,y_train, epochs=int(self.parent._ajustesEjecucion.value._fit_epochs.value), batch_size=int(self.parent._ajustesEjecucion.value._fit_batch_size.value), verbose=self.parent._ajustesEjecucion.value._fit_verbose.value, 
            validation_split=self.parent._ajustesEjecucion.value._fit_validation_split.value)

        except Exception as e:
            errorManager.error(self, "Error during model fit", e)

        sys.stdout = buffer = StringIO()

        print(self.parent._ajustesEjecucion.value._fit_epochs.value)

      
        model.summary()
        
        try:
             _, accuracy = model.evaluate(X_test, y_test, y)
             print('Accuracy: %.2f' % (accuracy*100))

        except Exception as e:
            errorManager.error(self, "Error during model evaluation", e)   

        result=buffer.getvalue()

        self.parent._output.value=result
        

        

class WindowLayerOrder(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.setAcceptDrops(True)
        
        self.blayout = QVBoxLayout()
        self.lista=[]
        self.father=parent
        
        
    def getLista(self):
        return self.lista
        

    def closeEvent(self, event):
        print("event ,aquí hay que ordernar la lista de vuelta")
        print(self.get_item_data())
        self.father.__setLayerLista(self.get_item_data())

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            data.append(w.data)
        return data
            

    def updateLista(self, lista):
        self.lista=lista
        self.clearLayout(self.blayout)
        for l in lista:
            item = DragButton()
            item.setText(l['self._name'])
            item.setData(l)
            self.blayout.addWidget(item)
        self.setLayout(self.blayout)
        

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if pos.x() < w.x() + w.size().width() // 2:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.blayout.insertWidget(n-1, widget)

                break

        e.accept()
    
    def dragEnterEvent(self, e):
        e.accept()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class DragButton(QPushButton):

    def __init__(self):
        super().__init__()
        self.data= None
        self.blayout = QHBoxLayout()

    def setData(self, item):
        self.data=item

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)