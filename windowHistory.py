from imports import *

class historyWindow(BaseWidget):
    def __init__(self):
        BaseWidget.__init__(self,'vHistorial')
        self.parent = None

        self.formset = [
            'h3:Historial',
           '_historial'
            ]    
        
        self._historial=ControlList()
        self._historial.add_popup_menu_option('rerun', function_action=self._do_something)
        self._historial += ('Ejecución1', 'Ejecución2')

    def _do_something(self):
        pass

