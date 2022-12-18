from imports import *
from sklearn import svm, datasets, metrics
from sklearn.model_selection import cross_val_score

class settingsWindow(BaseWidget):

    def __init__(self, type):
        BaseWidget.__init__(self,'Settings')
        self.parent = None

        self.type=type
        #print(type)
        #https://medium.com/@svanillasun/how-to-deal-with-cross-validation-based-on-knn-algorithm-compute-auc-based-on-naive-bayes-ff4b8284cff4
        #self._titulo.add_popup_menu_option('option 0', function_action=self._help)    
        #SKLEARN
        if(self.type=="SKLEARN"):
            #cross validation
            self._cv=ControlCombo('CV')
            self._cv.add_item('Integer')
            self._cv.add_item('Shuffle Split')

            self._cv.changed_event=self.__cv_Changed      
            self._cv_Integer=ControlNumber('cv Integer')
            #   shuffle cross validation
            self._shuffle_n_splits=ControlNumber('Shuffle n splits')
            self._shuffle_n_splits.hide()
            self._shuffle_n_splits.value=10
            self._shuffle_test_size=ControlNumber('Shuffle test size')
            self._shuffle_test_size.hide()
            self._shuffle_test_size.decimals=3
            self._shuffle_test_size.min=0.0
            self._shuffle_test_size.max=1.0
            self._shuffle_train_size=ControlNumber('Shuffle train size')
            self._shuffle_train_size.hide()
            self._shuffle_train_size.decimals=3
            self._shuffle_train_size.min=0.0
            self._shuffle_train_size.max=1.0
            self._shuffle_random_state=ControlNumber('Shuffle random state')
            self._shuffle_random_state.hide()
            #   scoring cross
            self._cv_scoring=ControlCombo('SK learn scoring')
            listaScores=metrics.get_scorer_names()
            for x in listaScores:
                self._cv_scoring.add_item(x)

            #train_test_split
            self._sk_train_test_split_test_size=ControlNumber('Train test split')
            self._sk_train_test_split_test_size.decimals=3
            self._sk_train_test_split_test_size.min=0.0
            self._sk_train_test_split_test_size.max=1.0
            self._sk_train_test_split_test_size.value=0.25
            self._sk_random_state=ControlNumber('Random state')
            self._sk_shuffle=ControlCheckBox('Shuffle train test split')

            self.formset = [
            'h3:cross validation', 
            '_cv','_cv_Integer',
            '_shuffle_n_splits', '_shuffle_test_size','_shuffle_train_size','_shuffle_random_state','=',
            'h3:scoring cross',
            '_cv_scoring','=',
            'h3:train_test_split',
            '_sk_train_test_split_test_size'
            ]   

        #SEQUENTIAL
        #compile
        else:
            print(self.type)

            self._seq_optimizers=ControlCombo('Compile optimizers')
            self._seq_optimizers.hide
            optiList=["Adadelta", "Adagrad", "Adam", "Adamax", "FTRL", "Nadam", "Optimizer", "RMSprop", "SGB"]
            for x in optiList:
                self._seq_optimizers.add_item(x)
            
            self._seq_loss=ControlCombo('Compile loss')
            self._seq_loss.hide
            lossList=["BinaryCrossentropy", "BinaryFocalCrossentropy", "CategoricalCrossentropy", "CategoricalHinge", "CosineSimilarity", "Hinge", "Hunge", "KLDivergence", "LogCosh", "Loss", "MeanAbsoluteError", "MeanAbsolutePercentageError", "MeanSquaredError", "MeanSquaredLogarithmicError", "Poisson", "Reduction", "SparseCategoricalCrossentropy", "SquaredHinge"]
            for x in lossList:
                self._seq_loss.add_item(x)

            self._seq_metrics=ControlCheckBoxList('Compile metrics')
            self._seq_metrics.hide
            metricList=["AUC", "Accuracy", "BinaryAccuracy", "BinaryCrossentropy", "BinaryIoU", 
            "CategoricalAccuracy", "CategoricalCrossentropy", "CategoricalHinge", "CosineSimilarity", "FalseNegatives", "FalsePositives", 
            "Hinge", "IoU", "KLDivergence", "LogCoshError", 
            "Mean", "MeanAbsoluteError", "MeanAbsolutePercentageError", "MeanIoU", "MeanMetricWrapper", "MeanRelativeError", "MeanSquaredError", "MeanSquaredLogarithmicError", "MeanTensor", 
            "Metric", "OneHotIoU", "OneHotMeanIoU", "Poisson", "Precision", "PrecisionAtRecall", "Recall", "RecallAtPrecision", "RootMeanSquaredError",     
            "SensitivityAtSpecificity", "SparseCategoricalAccuracy", "SparseCategoricalCrossentropy", "SparseTopKCategoricalAccuracy", "SpecificityAtSensitivity", 
            "SquaredHinge", "Sum", "TopKCategoricalAccuracy",    "TrueNegatives", "TruePositives"]

            listaMetrics=[]
            for x in metricList:
                listaMetrics.append((x,False))
            self._seq_metrics.value=listaMetrics
      
            self._seq_compile_steps_per_execution=ControlNumber('Compile steps per execution')

            #fit
            self._fit_batch_size=ControlNumber('Fit batch size')
            self._fit_batch_size.value=32
            self._fit_epochs=ControlNumber('Fit epochs')
            self._fit_epochs.value=20
            self._fit_verbose=ControlCombo('Verbose')
            self._fit_verbose.add_item('auto')
            self._fit_verbose.add_item('0')
            self._fit_verbose.add_item('1')
            self._fit_verbose.add_item('2')
            self._fit_validation_split=ControlNumber('Fit validation split')
            self._fit_validation_split.value=0.0
            self._fit_validation_split.min=0.0
            self._fit_validation_split.decimals=3
            self._fit_validation_split.max=1.0
            self._fit_initial_epoch=ControlNumber('Initial epoch')

            

            self.formset = [
            'h3:compile', 
            '_seq_optimizers','_seq_loss','_seq_metrics','_seq_compile_steps_per_execution','=',
            'h3:fit',
            '_fit_batch_size','_fit_epochs','_fit_verbose','_fit_validation_split','_fit_initial_epoch'
            ]   


        """
    def __update(self):
        print("update")
        if self.type=="SKLEARN":
            self._cv.show
        else:
            self._seq_optimizers.show
            self._seq_metrics.show
            self._seq_loss.show
        """








   

        

    def __cv_Changed(self):
        print(self.type)
        if(self._cv.value=='Integer'):
            
            self._cv_Integer.show()
            self._shuffle_n_splits.hide()
            self._shuffle_test_size.hide()
            self._shuffle_train_size.hide()
            self._shuffle_random_state.hide()
        else:
            self._cv_Integer.hide()
            self._shuffle_n_splits.show()
            self._shuffle_test_size.show()
            self._shuffle_train_size.show()
            self._shuffle_random_state.show()
       

    