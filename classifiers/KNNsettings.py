from imports import *
import sklearn

class KNNsettings(BaseWidget):
    def __init__(self, father, X,Y):
        BaseWidget.__init__(self,'KNN window')
        self.parent = father
        self._x=X
        self._y=Y


        self.topmost=True
       

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.numNeighbors=ControlNumber('number of nerighbots')
        #self.numNeighbors.decimals=3
        self.numNeighbors.max=10
        self.weights=ControlCombo(label='which weight')
        self.weights.add_item('uniform')
        self.weights.add_item('distance')

        self.algorithm=ControlCombo(label='algorith')
        self.algorithm.add_item('ball_tree')
        self.algorithm.add_item('kd_tree')
        self.algorithm.add_item('brute')
        self.algorithm.add_item('auto')

        self.leafSize=ControlNumber("Size of the leafs")
        self.mikowski=ControlNumber("Lo de Mikowski")
        #self.metric=ControlNumber("The distance metric to use for the tree")metricstr or callable, default=’minkowski’
        #self.metricParams=dict default none
        self.njobs=ControlNumber("The number of parallel jobs to run for neighbors search")
        
        #confString="0ua00"

        #self.config=ControlText("conf")
        #self.config.value=self.confString

        self.execute=ControlButton("Classify")
        self.execute.value=self._execute
        

        #self.config.changed_event=self.__updateReverse


        
        self.numNeighbors.changed_event=self.__update
        self.weights.changed_event=self.__update
        self.algorithm.changed_event=self.__update
        self.leafSize.changed_event=self.__update
        self.mikowski.changed_event=self.__update




    def __update(self):
        strBuild=""+ str(int(self.numNeighbors.value))
        if self.weights.value=='uniform':
            strBuild=strBuild+'u'
        else:
            strBuild=strBuild+'d'

        if self.algorithm.value=='ball_tree':
            strBuild=strBuild+'t'
        elif self.algorithm.value=='kd_tree':
            strBuild=strBuild+'k'
        elif self.algorithm.value=='brute':
            strBuild=strBuild+'b'
        else:
            strBuild=strBuild+'a'

        strBuild=strBuild+str(int(self.leafSize.value))+str(int(self.mikowski.value))
        self.confString=strBuild
        self.parent._updateConfig=str(self.confString)

    def __updateReverse(self, confString):
        self.numNeighbors.value=int(confString[0])
        if confString[1]=='u':
            self.weights.value='uniform'
        else:
            self.weights.value='distance'

        if confString[2]=='t':
            self.algorithm.value='ball_tree'
        elif confString[2]=='k':
            self.algorithm.value='kd_tree'
        elif confString[2]=='b':
            self.algorithm.value='brute'
        else:
            self.algorithm.value='auto'

        self.leafSize.value=int(confString[3])

        self.mikowski.value=int(confString[4])



    def _execute(self):
        
        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        
        self.parent.X=X
        self.parent.y=y
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

        
        X_train,X_test,y_train,y_test=train_test_split(self.parent.X,self.parent.y,test_size=0.2,random_state=4)
        neigh = neighbors.KNeighborsClassifier(n_neighbors=1)
        neigh.fit(X_train,y_train)

        y_predict=neigh.predict(X_test)

        result="El resultado de predicción es "+str(y_predict)
        #https://scikit-learn.org/stable/modules/model_evaluation.html            
        #confussion matrix
        
        matrix=confusion_matrix(y_test, y_predict)
        result=result+"\n"+"y la matriz de confusión" +"\n"+str(matrix)
        #[[16  0  0]
        #[ 0  4  1]
        #[ 0  1  8]]
    
        #accuracy score
        accuracy=sklearn.metrics.accuracy_score(y_test,y_predict)

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
        self.parent._output.value=result
        #self.parent._salida.value=result
        #self.parent.show()
        #self.parent._miniV.show()
        #self.parent._ajustesEjecucion.show()
        #self.parent._ejecucionesAnteriores.show()
        