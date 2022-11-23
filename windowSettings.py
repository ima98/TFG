from imports import *


class settingsWindow(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self,'Settings')
        self.parent = None

        self.formset = [
            'h4:Ajustes', '','=',
            '_cross','||',
            '_crossValidation', ''

            ]    

        self._titulo=ControlLabel('Ajustes tirar')

        #https://medium.com/@svanillasun/how-to-deal-with-cross-validation-based-on-knn-algorithm-compute-auc-based-on-naive-bayes-ff4b8284cff4
        #self._titulo.add_popup_menu_option('option 0', function_action=self._help)
        
        self._ejecAnteriores     = ControlCombo()
        self._titejec=ControlLabel('Ejecuciones anteriores')
        self._cross=ControlLabel('Cross')
        self._crossValidation = ControlNumber()

   

        

       

    