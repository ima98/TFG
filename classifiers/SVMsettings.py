from imports import *

class SVMsettings(BaseWidget):
    def __init__(self, father, X,Y):
        BaseWidget.__init__(self,'KNN window')
        self.parent = father
        self._x=X
        self._y=Y


        self.topmost=True

        

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.C=ControlNumber('Regularization parameter')
        self.kernel=ControlCombo(label='The kernel type')
        self.kernel.add_item('rbf')
        self.kernel.add_item('linear')
        self.kernel.add_item('poly')
        self.kernel.add_item('sigmoid')
        self.kernel.add_item('precomputed')


        self.degree=ControlNumber('Degree of the polynomial kernel function (‘poly’)')
        self.degree.hide
        

        self.gamma=ControlCombo(label='Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’')
        self.gamma.add_item('scale')
        self.gamma.add_item('auto')


        self.coef0=ControlNumber("only significant in ‘poly’ and ‘sigmoid’")
        self.shrinking=ControlCheckBox("The shrinking heuristic")
        self.probability=ControlCheckBox("enable probability estimates")
        self.tol=ControlNumber("Tolerance for stopping criterio")
        self.cache_size=ControlNumber("cache_size")

        self.class_weight=ControlCombo(label='class_weight')
        self.class_weight.add_item('dict')
        self.class_weight.add_item('balanced')

        self.verbose=ControlCheckBox("Enable verbose output")

        self.max_iter=ControlNumber("Hard limit on iterations")

        self.decision_function_shape=ControlCombo()
        self.decision_function_shape.add_item('ovo')
        self.decision_function_shape.add_item('ovr')

        self.break_ties=ControlCheckBox("breaking ties comes at a relatively high computational cost compared")

        self.random_state=ControlNumber("the pseudo random number generation")

        #self.metric=m
        #self.metricParams=mp
        #self.njobs=nj
        
        self.confString="0ua00"

        self.config=ControlText("conf")
        self.config.value=self.confString

        self.execute=ControlButton("Classify")
        self.execute.value=self._execute
        

        #self.config.changed_event=self.__updateReverse


        
        #self.numNeighbors.changed_event=self.__update
        #self.weights.changed_event=self.__update




    def _execute(self):
        
        #iris = datasets.load_iris()
        #X = iris.data[:, :2]  # we only take the first two features.
        #y = iris.target
        #clasi=KNN(4,'uniform',NULL, NULL, NULL, NULL, NULL, NULL)
        #neigh = neighbors.KNeighborsClassifier(n_neighbors=1)
        #X = [[0], [1], [2], [3]]
        #y = [0, 0, 1, 1]
        #samples = [[0., 0., 0.], [0., .5, 0.], [1., 1., .5]]
        #neigh.fit(X,y)
        #clasi.execute
        #self.parent._salida.value=neigh.kneighbors([[1., 1.]])

        #https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
        #iris=datasets.load_iris(return_X_y=True)
        #iris=self.parent.actualCSV
        #X=iris[0]
        
        #y=iris[1]
        X_train,X_test,y_train,y_test=train_test_split(self.parent.X,self.parent.y,test_size=0.2,random_state=4)
        svc = SVC(gamma='auto')
        svc.fit(X_train,y_train)

        y_predict=svc.predict(X_test)

        result="El resultado de predicción es "+str(y_predict)
        #https://scikit-learn.org/stable/modules/model_evaluation.html            
        #confussion matrix
        
        matrix=confusion_matrix(y_test, y_predict)
        result=result+"\n"+"y la matriz de confusión" +"\n"+str(matrix)
        #[[16  0  0]
        #[ 0  4  1]
        #[ 0  1  8]]
    
        #accuracy score
        #accuracy=accuracy_score(y_test,y_predict)

        #classification_report
        report=classification_report(y_test,y_predict)
        #report=              precision    recall  f1-score   support

        #   0       1.00      1.00      1.00        16
        #   1       0.80      0.80      0.80         5
        #   2       0.89      0.89      0.89         9

    #accuracy                           0.93        30
   #macro avg       0.90      0.90      0.90        30
#weighted avg       0.93      0.93      0.93        30

        hamming=hamming_loss(y_test, y_predict)
        #0.06666666666666667

        #jacc=jaccard_score(y_test,y_predict)
        self.parent._salida.value=report
        self.parent.show()
        self.parent._miniV.show()
        self.parent._ajustesEjecucion.show()
        self.parent._ejecucionesAnteriores.show()
        