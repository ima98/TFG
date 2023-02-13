from imports import *
import sklearn
import json
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit

class sklearnBase(BaseWidget):
    def __init__(self, father,sklearn):
        """ inicializa la ventana con los ajustes del clasificador
        
        :param father: ventana padre
        :param sklearn: nombre del clasificador
        
        """
        BaseWidget.__init__(self,'SKLEARN window')
        self.parent = father

        self.excepciones=['_parent_widget', '_mainmenu','_splitters','_tabs','_formset', '_formload','_formLoaded','_uid', '_execute',  '_saveModel','_generatePy']
        self.loadInputX=False
        self.loadInputY=False

        self.topmost=True       

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.name=sklearn

        self.intExcepciones=[]

        self.__loadJSONData(sklearn)

        self._saveModel=ControlButton('Save model')
        self._saveModel.value=self.__saveModel

        self._generatePy=ControlButton('Generate Py')
        self._generatePy.value=self.__generatePy

        self._execute=ControlButton('Execute')
        self._execute.value=self.__execute


        if self.parent._modelConfig is not None and self.parent._modelBoolean:
            try:
                self.__loadSettings(self.parent._modelConfig)
            except:
                None

        self.X_train=0
    

    def __loadJSONData(self, sklearn):
        import os
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__,sklearn+'.json')) as f:
            self.data= json.load(f)

        for key,value in self.data.items():
            self.translate(key, value)

    def __updateReverse(self, confString):
        self.numNeighbors.value=int(confString[0])


    def __saveModel(self):
        """guarda el modelo en archivo h5

        """
        import h5py
        l=self.__getConfig()
        dic=dict(l)
        m=dic["constructor"]

        if(self.loadInputX==True and self.loadInputY==True):
            parts=m.partition('(')
            newC=parts[0]+'(X_train, y_train, '+parts[2]
            m=newC
        elif(self.loadInputX==True and self.loadInputY==False):
            parts=m.partition('(')
            newC=parts[0]+'(X_train, '+parts[2]
            m=newC
                
        m2='self.modelo='+m
        exec(m2)
        
        with h5py.File('filename', 'w') as hf:
            hf.create_dataset("coef",  data=self.modelo.coef_)
            hf.create_dataset("intercept",  data=self.modelo.intercept_)
            hf.create_dataset("classes", data=self.modelo.classes_)

    def translate(self, name,tipoJson):
        """transforma una tupla de key y value a un botón

        :param name: llave del diccionario
        :param tipoJson: valor del diccionario
        """
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
        """Carga los valores del diccionario en los botones

        :param dic: diccionario
        """

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
        """Generá una lista con los botones y sus valores
        :return: (list) devuelve la lista generada
        """
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
        """Añade la ejecución al historial de ejecuciones

        :param l: lista con la configuración
        """
        import datetime
        addH=l
        addH[:0] = [('type',self.name)]
        AddHD=dict(addH)
        now = datetime.datetime.now()
        self.parent._listaAnteriores.value.listaHistorial.append(((self.name+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'-'+str(now.microsecond)), AddHD))
        self.parent._listaAnteriores.value.__update()

    def __generatePy(self):
        """Llama al generador de código con las variables
        """
        import fileGenerator
        toAdd=""

        train_test_splitList=[self.parent._ajustesEjecucion.value._sk_train_test_split_test_size.value,
            self.parent._ajustesEjecucion.value._sk_random_state.value, self.parent._ajustesEjecucion.value._sk_shuffle.value]


        l=self.__getConfig()
        dic=dict(l)    
        constructor=dic["constructor"]

        fileGenerator.fileGeneratorSKlearn(self.parent.fileName, train_test_splitList, constructor)


    def __execute(self):
        """Genera el clasificador y lo ejecuta
        """

            
            #from sklearn.datasets import load_iris

            #iris = load_iris()
            #X = iris.data[:, :2]  # we only take the first two features.
            #y = iris.target
        import errorManager
        from numpy import fromstring
        try:
            import helper
            (X,y,_)=helper.getDataSet(self.parent.fileName)

   
        except Exception as e: 
            errorManager.error(self, "Error loading the csv", e)
            return

        from sklearn.linear_model import LinearRegression


            #https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html

            #https://medium.com/dunder-data/from-pandas-to-scikit-learn-a-new-exciting-workflow-e88e2271ef62
        l=self.__getConfig()
        dic=dict(l)

        addH=l
        addH[:0] = [('type',self.name)]
        AddHD=dict(addH)
        self.parent._miniV.value._loadModelString.value=json.dumps(AddHD)

        m=dic["constructor"]

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

            
        from sklearn.model_selection import train_test_split, StratifiedKFold
        if(self.parent._ajustesEjecucion.value._testOptionsCombo.value=='Cross-validation'):
            skf=StratifiedKFold(n_splits=int(self.parent._ajustesEjecucion.value._StratifiedKFoldNSplits.value), shuffle=self.parent._ajustesEjecucion.value._StratifiedKFoldShuffle.value, random_state=None)
            lst_accu_stratified = []
            lst_cross_val_score_stratified = []
            lst_y_predict_stratified = []
            lst_matrix_stratified =[]
            lst_accuracyScore_stratified=[]
            lst_report_stratified=[]

            for i, (train_index, test_index) in enumerate(skf.split(X, y)): 
                X_train_fold, X_test_fold = X.iloc[train_index], X.iloc[test_index] 
                y_train_fold, y_test_fold = y.iloc[train_index], y.iloc[test_index]

                try: 
                    self.modelo.fit(X_train_fold, y_train_fold)
                except Exception as e: 
                    errorManager.error(self, "Error during fit", e)
                    return

                try:
                    lst_accu_stratified.append(self.modelo.score(X_test_fold, y_test_fold))
                except Exception as e: 
                    errorManager.error(self, "Error during score", e)

                try:
                    if(self.parent._ajustesEjecucion.value._cv.value=="Integer"):
                        scores=cross_val_score(self.modelo, X_train_fold, y_train_fold, cv= int(self.parent._ajustesEjecucion.value._cv_Integer.value))
                    else:  
                        cvTemp = ShuffleSplit(n_splits=int(self.parent._ajustesEjecucion.value._shuffle_n_splits.value), test_size=self.parent._ajustesEjecucion.value._shuffle_test_size.value,
                        random_state=int(self.parent._ajustesEjecucion.value._shuffle_random_state.value))
                        scores=cross_val_score(self.modelo, X_train_fold, y_train_fold, cv= cvTemp)
                    lst_cross_val_score_stratified.append(scores)
                except Exception as e: 
                    errorManager.error(self, "Error during cross validation score", e)

                try:
                    y_predict=self.modelo.predict(X_test_fold)
                    lst_y_predict_stratified.append(y_predict)


                    try:
                        lst_matrix_stratified.append(sklearn.metrics.confusion_matrix(y_test_fold,y_predict))

                    except Exception as e: 
                        errorManager.error(self, "Error during confusion matrix", e) 

                    try:
                        lst_accuracyScore_stratified.append(sklearn.metrics.accuracy_score(y_test_fold,y_predict))
                    except Exception as e: 
                        errorManager.error(self, "Error during accuracy score", e) 

                    try:
                        lst_report_stratified.append(sklearn.metrics.classification_report(y_test_fold,y_predict))
                    except Exception as e: 
                        errorManager.error(self, "Error during metrics classification report", e) 
                except Exception as e: 
                    errorManager.error(self, "Error during prediction", e) 

            newLine="---------------------------------------------------------------\n"

            """
            for i in range(int(self.parent._ajustesEjecucion.value._StratifiedKFoldNSplits.value)):
                print(i)
                result=result+"Fold "+ str(i)+" information: \n"
                if(lst_accu_stratified!=[]):
                    result=result+"Score of the fold "+str(i+1)+": \n"+str(lst_accu_stratified[i])+'\n'
                    
                    
                if(lst_y_predict_stratified!=[]):
                    result=result+"Prediction of the fold "+str(i+1)+": \n"+str(lst_y_predict_stratified[i])+'\n'

                if(lst_matrix_stratified !=[]):
                    result=result+"Confusion matric of the fold "+str(i+1)+": \n"+str(lst_matrix_stratified[i])+'\n'

                if(lst_accuracyScore_stratified!=[]):
                    result=result+"Accuracy score of the fold "+str(i+1)+": \n"+str(lst_accuracyScore_stratified[i])+'\n'

                if(lst_report_stratified!=[]):
                    result=result+"Classification report score of the fold "+str(i+1)+": \n"+str(lst_report_stratified[i])+'\n'


                result=result+newLine

                self.parent._output.value=result

                return
            """
            

            if(lst_accu_stratified!=[]):
                    result=result+"List of the scores\n"
                    for i,x in enumerate(lst_accu_stratified):
                        result=result+"Fold "+str(i+1)+" score: "+str(x)+'\n'
                    result=result+newLine
                    
            if(lst_y_predict_stratified!=[]):
                    result=result+"List of the predictions\n"
                    for i,x in enumerate(lst_y_predict_stratified):
                        result=result+"Fold "+str(i+1)+" prediction: "+str(x)+'\n'
                    result=result+newLine

            if(lst_matrix_stratified !=[]):
                    result=result+"List of the confusion matrix\n"
                    for i,x in enumerate(lst_matrix_stratified):
                        result=result+"Fold "+str(i+1)+" matrix: \n"+str(x)+'\n'
                    result=result+newLine

            if(lst_accuracyScore_stratified!=[]):
                    result=result+"List of the accuracy scores\n"
                    for i,x in enumerate(lst_accuracyScore_stratified):
                        result=result+"Fold "+str(i+1)+" accuracy score: "+str(x)+'\n'
                    result=result+newLine

            if(lst_report_stratified!=[]):
                    result=result+"List of the classification reports\n"
                    for i,x in enumerate(lst_report_stratified):
                        result=result+"Fold "+str(i+1)+" classification report: \n"+str(x)+'\n'
                    result=result+newLine
            self.parent._output.value=result

            return

        else:
            X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=self.parent._ajustesEjecucion.value._sk_train_test_split_test_size.value,
            random_state=int(self.parent._ajustesEjecucion.value._sk_random_state.value), shuffle=self.parent._ajustesEjecucion.value._sk_shuffle.value)
   
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
            