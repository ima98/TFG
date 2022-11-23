from imports import *
class helpWindow(BaseWidget):

    def __init__(self, str):
        BaseWidget.__init__(self,'ParamKNN')
        self.parent = None

        self.formset = [
            #'h3:Parámetros del KNN',
            '_descripcion'
            ]

        if str=='KNN':
            self._decripcion=ControlLabel('KNN prueba')


        

       