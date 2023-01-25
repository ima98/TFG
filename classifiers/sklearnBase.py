from imports import *
import sklearn
import json
from modelConfig import *
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit

class sklearnBase(BaseWidget):
    def __init__(self, father,sklearn):
        BaseWidget.__init__(self,'SKLEARN window')
        self.parent = father


        self.excepciones=['_parent_widget', '_mainmenu','_splitters','_tabs','_formset', '_formload','_formLoaded','_uid', '_addLayer',  '_saveModel','_generatePy']
        self.loadInputX=False
        self.loadInputY=False


        self.topmost=True
       
        self.modelConfig=modelConfig(0, "sklearn")

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.name=sklearn

        self.intExcepciones=[]

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__,sklearn+'.json')) as f:
            self.data= json.load(f)

        for key,value in self.data.items():
            self.translate(key, value)

        self._addLayer=ControlButton('execute')
        self._addLayer.value=self.__execute


        self._saveModel=ControlButton('Save model')
        self._saveModel.value=self.__saveModel

        self._generatePy=ControlButton('Generate Py')
        self._generatePy.value=self.__generatePy


        if self.parent._modelConfig is not None and self.parent._modelBoolean:
            self.__loadSettings(self.parent._modelConfig)

        self.X_train=0
    

    def __updateReverse(self, confString):
        self.numNeighbors.value=int(confString[0])


    def __saveModel(self):
        l=self.__getConfig()
        l[:0] = [('type',self.name)]
        dic=dict(l)
        
        with open('result.json', 'w') as fp:
            json.dump(dic, fp)

    def translate(self, name,tipoJson):
        
        s=name
        if(tipoJson[0]=='Integer'):
            excep='_'+s
            self.intExcepciones.append(excep)
            m='self._'+s+'=ControlNumber('+"'"+s+"'"+')'
            exec(m)
            m2='self._'+s+'.decimals=0'
            exec(m2)
            if(len(tipoJson)>2):
                m1='self._'+s+'.min= '+str(tipoJson[1])
                m2='self._'+s+'.max= '+str(tipoJson[2])
                m3='self._'+s+'.value= '+str(tipoJson[1]) 
                exec(m1)
                exec(m2)
                exec(m3)
            elif(len(tipoJson)>1):
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

        elif(tipoJson[0]=='InputX'):
            self.loadInputX=True
        elif(tipoJson[0]=='InputY'):
            self.loadInputY=True
            


    def __loadSettings(self, dic):
        dic=dict(dic)
        for x, y in dic.items():
            if x not in ["type", "constructor"]:
                try:               
                    m=x+'.value='+"'"+str(y)+"'"
                    
                    exec(m)
                except:
                    m=x+'.value='+str(y)
                    
                    exec(m)


    def __getConfig(self):
        varAll=vars(self)
        lista=[]
        for var in varAll:
            if var.startswith("_") and var not in self.excepciones:
                
                if var in self.intExcepciones:
                    m='lista.append(("self.'+var+'",int(self.'+var+'.value)))'
                else:
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
                    cons=cons+name+"= "+str(tuplaLista[1])+", "

        cons=cons[:-2]
        cons=cons+")"


        lista.append(("constructor", cons))
        
        return lista


    def __addToHist(self, l):
        import datetime
        addH=l
        addH[:0] = [('type',self.name)]
        AddHD=dict(addH)
        now = datetime.datetime.now()
        self.parent._listaAnteriores.value.listaHistorial.append(((self.name+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'-'+str(now.microsecond)), AddHD))
        self.parent._listaAnteriores.value.__update()

    def __generatePy(self):
        import fileGenerator
        toAdd=""


        #listaMetrics=self.__getListaMetrics()
        #compileList=[self.parent._ajustesEjecucion.value._seq_optimizers.value, self.parent._ajustesEjecucion.value._seq_loss.value, int(self.parent._ajustesEjecucion.value._seq_compile_steps_per_execution.value),
        #    listaMetrics]

        train_test_splitList=[self.parent._ajustesEjecucion.value._sk_train_test_split_test_size.value,
            self.parent._ajustesEjecucion.value._sk_random_state.value, self.parent._ajustesEjecucion.value._sk_shuffle.value]


        l=self.__getConfig()
        dic=dict(l)    
        constructor=dic["constructor"]

        fileGenerator.fileGeneratorSKlearn(self.parent.fileName, train_test_splitList, constructor)


    def __execute(self):
            

            
            #from sklearn.datasets import load_iris

            #iris = load_iris()
            #X = iris.data[:, :2]  # we only take the first two features.
            #y = iris.target
            """
            from numpy import loadtxt
            dataset = loadtxt(self.parent.fileName, delimiter=',', dtype=int)

            
            

            # split into input (X) and output (y) variables
            X = dataset[:,0:dataset.shape[1]-1]
            y = dataset[:,dataset.shape[1]-1]
            


            iris = datasets.load_iris()
            X = iris.data[:, :4]  # we only take the first two features.
            y = iris.target
"""
            import errorManager
            try:

                from pandas import read_csv

                inputData = read_csv(self.parent.fileName, delimiter=',', header=1)

                y = inputData.iloc[:,inputData.shape[1]-1]

                

                X=inputData.iloc[:, 0:inputData.shape[1]-2]

                
            except Exception as e: 
                errorManager.error(self, "Error loading the csv", e)

            from sklearn.linear_model import LinearRegression


            #https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html

            #https://medium.com/dunder-data/from-pandas-to-scikit-learn-a-new-exciting-workflow-e88e2271ef62

            
            from sklearn.model_selection import train_test_split
            X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=self.parent._ajustesEjecucion.value._sk_train_test_split_test_size.value,
            random_state=int(self.parent._ajustesEjecucion.value._sk_random_state.value), shuffle=self.parent._ajustesEjecucion.value._sk_shuffle.value)



            l=self.__getConfig()
            dic=dict(l)

            
            m=dic["constructor"]

            from numpy import fromstring


            if(self.loadInputX==True and self.loadInputY==True):

                parts=m.partition('(')
                newC=parts[0]+'(X_train, y_train, '+parts[2]
                m=newC
            elif(self.loadInputX==True and self.loadInputY==False):
                parts=m.partition('(')
                newC=parts[0]+'(X_train, '+parts[2]
                m=newC
                

            result=""

            self.modelo=LinearRegression()

            m2='self.modelo='+m
            exec(m2)


            self.__addToHist(l)


            
            try:
                self.modelo.fit(X_train,y_train)
            except Exception as e: 
                errorManager.error(self, "Error during fit", e)
                
            
            
            try:
                if(self.parent._ajustesEjecucion.value._cv.value=="Integer"):
                    scores=cross_val_score(self.modelo, X_train, y_train, cv= int(self.parent._ajustesEjecucion.value._cv_Integer.value))
                else:  
                    cvTemp = ShuffleSplit(n_splits=int(self.parent._ajustesEjecucion.value._shuffle_n_splits.value), test_size=self.parent._ajustesEjecucion.value._shuffle_test_size.value,
                    random_state=int(self.parent._ajustesEjecucion.value._shuffle_random_state.value))
                    scores=cross_val_score(self.modelo, X_train, y_train, cv= cvTemp)
                result="Scores: "+"\n"+str(scores)               
            except Exception as e:
                errorManager.error(self, "Error during score calculation", e)
                

            #OUTPUT
            try:
                params=self.modelo.get_params
            
                result=result+"Model params :" +"\n"+str(params)
            except:
                None


            #predicción de las variables
            y_predict=self.modelo.predict(X_test) 

            result=result+"Prediction: "+str(y_predict)
            #https://scikit-learn.org/stable/modules/model_evaluation.html            
            #confussion matrix

            
            matrix=sklearn.metrics.confusion_matrix(y_test, y_predict)
            result=result+"\n"+"Confusion matrix" +"\n"+str(matrix)
            #[[16  0  0]
            #[ 0  4  1]
            #[ 0  1  8]]
        
            #accuracy score
            accuracy=sklearn.metrics.accuracy_score(y_test,y_predict)
            result=result+"\n"+"Accuracy matrix" +"\n"+str(accuracy)

            #classification_report
            report=sklearn.metrics.classification_report(y_test,y_predict)
            result=result+"\n"+"Classification report" +"\n"+str(report)

            #hamming=hamming_loss(y_test, y_predict)
            #0.06666666666666667

            #jacc=jaccard_score(y_test,y_predict)
            #exec('self.parent._output.value=result')

            self.parent._output.value=result
            