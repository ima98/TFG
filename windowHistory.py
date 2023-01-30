from imports import *
import datetime
import json
class historyWindow(BaseWidget):
    def __init__(self, parent):
        BaseWidget.__init__(self,'vHistorial')
        self.parent = parent

        self.listaHistorial=[]

        self.formset = [
            'h3:Historial',
           '_historial'
            ]    
        
        self._historial=ControlList()
        self._historial.readonly=True
        self._historial.add_popup_menu_option('reload', function_action=self.__reload)
        self._historial.add_popup_menu_option('save', function_action=self.__save)
        self._historial.add_popup_menu_option('load from file', function_action=self.__loadFromFile)

        now = datetime.datetime.now()

       


    def __save(self):
        now = datetime.datetime.now()
        for (x,y) in self.listaHistorial:
            if(x==str(self._historial.get_currentrow_value()[0])):
                data= json.dumps(y, indent=2)
                s='./executions/'+x+'.json'
                with open(s, "w") as outfile:
                    outfile.write(data)

    def __reload(self):
         for (x,y) in self.listaHistorial:
            if(x==str(self._historial.get_currentrow_value()[0])): 
                data=y
                self.parent._modelConfig=data
                self.parent._modelBoolean=True

                try:
                    data=dict(y)
                    tempDict=data
                    X=data['type']
                except:
                    data=y
                    tempDict=data[0]
                    X=tempDict['type']
                self.parent._showClassifierParams(X)
                self.parent._miniV.value._loadModelString.value=str(tempDict)


    def __loadFromFile(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        with open(file_path) as json_file:
            data = json.load(json_file)
            self.parent._modelConfig=data
            self.parent._modelBoolean=True
            try:
                X=data['type']
            except:
                tempDict=data[0]
                X=tempDict['type']
            self.parent._showClassifierParams(X)

    def _sklearnBase__update(self):
        self._historial.clear()
        for count,value in enumerate(self.listaHistorial):
            self._historial.__add__(' ')
            self._historial.set_value(0,count, value[0])
        self._historial.resize_rows_contents()


    def _sequentialModel__update(self):
        self._historial.clear()
        for count,value in enumerate(self.listaHistorial):
            self._historial.__add__(' ')
            self._historial.set_value(0,count, value[0])
        self._historial.resize_rows_contents()


    def __addValue(self, value):
        self._historial.__add__('a')
        self._historial.set_value(0,1,value)
