from imports import *
import sklearn
import json
from modelConfig import *
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit

class sklearnBase(BaseWidget):
    def __init__(self, father, X,Y, sklearn):
        BaseWidget.__init__(self,'SKLEARN window')
        self.parent = father
        self.x=X
        self.y=Y

        self.topmost=True
       
        self.modelConfig=modelConfig(0, "sklearn")

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.name=sklearn

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__,sklearn+'.json')) as f:
            self.data= json.load(f)

        for key,value in self.data.items():
            self.translate(key, value)

        self._addLayer=ControlButton('execute')
        self._addLayer.value=self.__execute

        if self.parent._listaConfig!=[] and self.parent._modelBoolean:
            self.__loadSettings(self.parent._listaConfig[1:])

    

    def __updateReverse(self, confString):
        self.numNeighbors.value=int(confString[0])


    def translate(self, name,tipoJson):
        #print(tipoJson)
        s=name
        if(tipoJson[0]=='Integer'):
            m='self._'+s+'=ControlNumber('+"'"+s+"'"+')'
            exec(m)
            if(len(tipoJson)>1):
                m1='self._'+s+'.value= '+str(tipoJson[1])
                exec(m1)               
            
        elif(tipoJson[0]=='Float'):
            m='self._'+s+'=ControlNumber('+"'"+s+"'"+')'
            exec(m)
            d='self._'+s+'.decimals=3'
            exec(d)
            if(len(tipoJson)>2):
                m1='self._'+s+'.min= '+str(tipoJson[1])
                m2='self._'+s+'.max= '+str(tipoJson[2])
                exec(m1)
                exec(m2)
            elif(len(tipoJson)>1):
                m1='self._'+s+'.value= '+str(tipoJson[1])  
                exec(m1) 
            
        
        elif(tipoJson[0]=='Combo'):
            m='self._'+s+'=ControlCombo('+"'"+s+"'"+')'
            exec(m)
            combo=tipoJson[1:]
            for x in combo:
                m='self._'+s+'.add_item('+"'"+x+"'"+')'
                exec(m)

        elif(tipoJson[0]=='Boolean'):
            m='self._'+s+'=ControlCheckBox('+"'"+s+"'"+')'
            exec(m)


    def __loadSettings(self, lista):
        excepciones=['_parent_widget', '_mainmenu','_splitters','_tabs','_formset', '_formload','_formLoaded','_uid', '_addLayer']
        varAll=vars(self)
        #print(lista)
        for var in varAll:
            if var.startswith("_") and var not in excepciones:
                    a=lista.pop(0)
                    try:
                        m='self.'+var+'.value='+"'"+str(a)+"'"
                        exec(m)
                    except:
                        m='self.'+var+'.value='+str(a)
                        exec(m)                 
            
                    
        

    def __getConfig(self):
        excepciones=['_parent_widget', '_mainmenu','_splitters','_tabs','_formset', '_formload','_formLoaded','_uid', '_addLayer']
        varAll=vars(self)
        lista=[]
        for var in varAll:
            if var.startswith("_") and var not in excepciones:
    
                m='lista.append(("self.'+var+'",self.'+var+'.value))'
                exec(m)

        cons=self.data["constructor"]
        cons=cons[:-1]
        

        for tuplaLista in lista:
            if(tuplaLista[0]!="self._name"):
                name=tuplaLista[0][6:]
                try:
                    cons=cons+name+"= '"+tuplaLista[1]+"', "
                except:
                    cons=cons+name+"= "+str(int(tuplaLista[1]))+", "
        
        cons=cons[:-2]
        cons=cons+")"
        lista.append(("constructor", cons))
        print(lista)
        return lista


    def __dicFloatToInt(self, dic):
        lista=[]
        for x in dic:
            try:
                x[1]=int(x[1])
                lista.append(x)
            except:
                lista.append(x)
        print(lista)
        return dict(lista)


    def __execute(self):
        l=self.__getConfig()
        dic=dict(l)

        
        #from sklearn.datasets import load_iris

        #iris = load_iris()
        #X = iris.data[:, :2]  # we only take the first two features.
        #y = iris.target
        from numpy import loadtxt
        dataset = loadtxt(self.parent.fileName, delimiter=',')

        
        

        # split into input (X) and output (y) variables
        X = dataset[:,0:dataset.shape[1]-1]
        y = dataset[:,dataset.shape[1]-1]
        
        #clasi=KNN(4,'uniform',NULL, NULL, NULL, NULL, NULL, NULL)
        #neigh = neighbors.KNeighborsClassifier(n_neighbors=1)
        #X = [[0], [1], [2], [3]]
        #y = [0, 0, 1, 1]
        #samples = [[0., 0., 0.], [0., .5, 0.], [1., 1., .5]]
        #neigh.fit(X,y)
        #clasi.execute
        #self.parent._salida.value=neigh.kneighbors([[1., 1.]])

        #https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html

        #https://medium.com/dunder-data/from-pandas-to-scikit-learn-a-new-exciting-workflow-e88e2271ef62

        from sklearn.model_selection import train_test_split
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=self.parent._ajustesEjecucion.value._sk_train_test_split_test_size.value,
        random_state=int(self.parent._ajustesEjecucion.value._sk_random_state.value), shuffle=self.parent._ajustesEjecucion.value._sk_shuffle.value)


          
        m=dic["constructor"]
        #modelo = neighbors.KNeighborsClassifier(n_neighbors=1)


        m2='modelo='+m
        #print(m2)
        exec(m2)
        m3="modelo.fit(X_train,y_train)"
        import errorManager
        try:
            exec(m3)
        except Exception as e: 
            errorManager.error(self, "Error during fit", e)
            print(e)
        
        if(self.parent._ajustesEjecucion.value._cv.value=="Integer"):
            m4="scores=cross_val_score(modelo, X_train, y_train, cv= int(self.parent._ajustesEjecucion.value._cv_Integer.value))"
        else:  
            m4="scores=cross_val_score(modelo, X_train, y_train, cv= int(self.parent._ajustesEjecucion.value._cv_scoring.value))"

        try:
            exec(m4)
            print("scores:     ")
            exec("print(scores)")
        except Exception as e:
            errorManager.error(self, "Error during score calculation", e)
            print(e)

        #exec('y_predict=modelo.predict(X_test)')



        #exec('result="El resultado de predicción es "+str(y_predict)')
        #https://scikit-learn.org/stable/modules/model_evaluation.html            
        #confussion matrix

        
        #exec('matrix=confusion_matrix(y_test, y_predict)')
        #exec('result=result+"\n"+"y la matriz de confusión" +"\n"+str(matrix)')
        #[[16  0  0]
        #[ 0  4  1]
        #[ 0  1  8]]
    
        #accuracy score
        #exec('accuracy=sklearn.metrics.accuracy_score(y_test,y_predict)')

        #classification_report
        #exec('report=classification_report(y_test,y_predict)')
        #report=              precision    recall  f1-score   support

        #   0       1.00      1.00      1.00        16
        #   1       0.80      0.80      0.80         5
        #   2       0.89      0.89      0.89         9

    #accuracy                           0.93        30
   #macro avg       0.90      0.90      0.90        30
#weighted avg       0.93      0.93      0.93        30

        #hamming=hamming_loss(y_test, y_predict)
        #0.06666666666666667

        #jacc=jaccard_score(y_test,y_predict)
        #exec('self.parent._output.value=result')
    

        
        