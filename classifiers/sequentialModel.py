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
    def __init__(self, father, X,Y):
        self.parent=father
        
        self.model=Sequential()
        self.model.add(Dense(12, input_shape=(8,), activation='relu'))
        BaseWidget.__init__(self,'Sequential mode')
        
        self.layers=[]
        self.layersConfig=[]
        
        self._layerType=ControlCombo('layer types')
        root = "./classifiers/layers"
        for item in os.listdir(root):
            if os.path.isfile(os.path.join(root, item)):
                if item.endswith('.json'):
                    print(item)
                    left_text = item.partition(".")[0]
                    self._layerType.add_item(left_text)


        #self._layerType.add_item('prueba')
        
        self._layerCombo=ControlCombo('layers')
        #self._layerCombo.add_item('de prueba')
        #self._layerCombo.changed_event=self.__editLayer
        
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

        self.formset=['_layerType','_addLayer', '_layer','_layerCombo','_layerEdit',('_deleteLayer', '_editLayer', '_editLayerOrder'),('_generatePy'),'_execute']
        

        if self.parent._listaConfig!=[] and self.parent._modelBoolean:
            self.__loadSettings(self.parent._listaConfig[1:])
        
    
    def __addLayer(self):
        self._layerEdit.hide()
        self._layer.show()
        #if(self._layerType.value=='ltsm'):
        #    prueba=ltsm()
        #    prueba.parent=self
        #    self._layer.value=prueba
        #elif(self._layerType.value=='Dense'):
        #    prueba=dense()
        #    prueba.parent=self
        #    self._layer.value=prueba
        prueba=layer(self._layerType.value, self)
        
        prueba.parent=self
        self._layer.value=prueba
        
        
                
    def __addLayerToModel(self, l):
        self.layers.append(l)
        #self.parent._modelConfig=self.layers
        self._layerCombo.add_item(l['_name'],l)
        self._layer.hide()
        #self.model.add(l)
        #self.parent.nextInputSize=l.output_shape
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
        #self._layerCombo.value=dic
        for item in self.layers:
            if item['self._name']==dic['self._name']:
                self.layers[self.layers.index(item)]=dic
        
        #print("lista")
        #print(self.layers)
        self._layerEdit.hide()
        
        
        self.__generateComboFromList()

        

    def __editLayer(self):
        self._layer.hide()
        self._layerEdit.show()
        prueba=layer(self._layerType.value, self, self._layerCombo.value)
        prueba.parent=self
        self._layerEdit.value=prueba

    
    def __generateComboFromList(self):
        #print(self._layerCombo.value)
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self._layerCombo.clear()
        for layerDic in self.layers:
            #print(layerDic)
            #dic['self._name'],dic
            self._layerCombo.add_item(layerDic['self._name'], layerDic)
        #print(self._layerCombo.items)
        
    def __generatePy(self):
        fname='generated.py'
        with open(fname, 'w') as f:
            f.write("import tensorflow as tf")
            f.write('\n')
            f.write("dataset = loadtxt("+"'"+'diabetes.csv'+"'"+", delimiter=',')")
        f.close()

    def __execute(self):

        dataset = loadtxt(self.parent.fileName, delimiter=',')

        
        

        # split into input (X) and output (y) variables
        X = dataset[:,0:dataset.shape[1]-1]
        y = dataset[:,dataset.shape[1]-1]
        model = Sequential()

        for layerDic in self.layers:
            cons=layerDic['constructor']
            m='layerTemp='+cons
            exec(m)
            exec("model.add(layerTemp)")
            

        """
        model.add(Dense(8, activation='relu'))
        model.add(Dense(12, input_shape=(8,), activation='relu'))
        
        model.add(Dense(1, activation='sigmoid'))
        """
        #sys.stdout = buffer = StringIO()
        
        try:
            listaMetrics=self.parent._ajustesEjecucion.value._seq_metrics.items
            l2=[]
            for x in listaMetrics:
                if x[1]==True:
                    l2.append(x[0])
            print(l2)
            model.compile(optimizer='rmsprop', metrics=['Accuracy'])
            #model.compile(optimizer=self.parent._ajustesEjecucion.value._seq_optimizers.value, loss=self.parent._ajustesEjecucion.value._seq_loss.value, steps_per_execution=self.parent._ajustesEjecucion.value._seq_compile_steps_per_execution.value,
            #metrics=l2)
        except:
            print("There was some error with the fit, using default compile")
            model.compile(optimizer='rmsprop', metrics=['Accuracy'])


        print("PRIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIINT")
        print(self.parent._ajustesEjecucion.value._fit_epochs.value)

        #FIT
        try:
            model.fit(X,y, epochs=int(self.parent._ajustesEjecucion.value._fit_epochs.value), batch_size=int(self.parent._ajustesEjecucion.value._fit_batch_size.value), verbose=self.parent._ajustesEjecucion.value._fit_verbose.value, 
            validation_split=self.parent._ajustesEjecucion.value._fit_validation_split.value)

        except:
            print("There was some error with the fit, using default fit")
            model.fit(X, y, epochs=20, batch_size=10)
        
        #result=buffer.getvalue()
        result=""

        _, accuracy = model.evaluate(X, y)
        
        print('Accuracy: %.2f' % (accuracy*100))
        #result=result+"\n And the accuracy: "+buffer.getvalue()
        model.summary()
        #result=result+"\n And the summary: "+buffer.getvalue()

        self.parent._output.value=result
        

        """
        dataset = loadtxt('diabetes.csv', delimiter=',')
        X = dataset[:,0:8]
        y = dataset[:,8]

        #https://www.tensorflow.org/api_docs/python/tf/keras/Model
        #variables del compile
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.fit(X, y, epochs=150, batch_size=10)
        
        
        _, accuracy = self.model.evaluate(X, y)
        self.parent._output.value=accuracy
        
        for x in self.layers:
            self.model.add(x)
            """

    def __loadSettingsFromModel(self, lista):
        self.layers=lista
        

class WindowLayerOrder(QWidget):

    def __init__(self, parent):
        super().__init__()
        
        self.setAcceptDrops(True)
        self.blayout = QHBoxLayout()
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