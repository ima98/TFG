from imports import *

class MLPsettings(BaseWidget):
    def __init__(self, father, X,Y):
        BaseWidget.__init__(self,'MLP window')
        self.parent = father
        
        self._hidden_layer_sizes=ControlNumber('hidden layer sizes')
        
        self._activation=ControlCombo('activation')
        self._activation.add_item('identity')
        self._activation.add_item('logistic')
        self._activation.add_item('tanh')
        self._activation.add_item('relu')
        
        self._solver=ControlCombo('solver')
        self._solver.add_item('lbfgs')
        self._solver.add_item('sgd')
        self._solver.add_item('adam')
        
        self._alpha=ControlNumber('alpha')
        self._batch_size=ControlNumber('batch_size')
        
        self._learning_rate=ControlCombo('learning rate')
        self._learning_rate.add_item('constant')
        self._learning_rate.add_item('invscaling')
        self._learning_rate.add_item('adaptive')
        
        self._learning_rate_init=ControlNumber('learning rate init')
        