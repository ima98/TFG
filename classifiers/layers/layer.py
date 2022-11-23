from imports import *
import json

import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras import layers

from keras.models import Sequential
from keras.layers import Dense, Dropout


class layer(BaseWidget):
    def __init__(self, *args): 
        #args[0] layertype, args[1] father, args[2] optional dic
        BaseWidget.__init__(self,'keras layer')


       

        self.parent=args[1]

        self.topmost=True
        
        #self.setMinimumWidth(400)
        #self.setMinimumHeight(300)
       
        self.layerType=args[0]
        
        self._name=ControlText('name')
        if(len(args) > 2):
            self._name.readonly=True

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__,self.layerType+'.json')) as f:
            self.data= json.load(f)

        for key,value in self.data.items():
            self.translate(key, value)

        #self._addLayer=ControlButton('add layer')
        #self._addLayer.value=self.__addLayer

        
        if(len(args) > 2):
            print("entra en los args")
            print(args[2])
            self.__setValuesFromDic(args[2])
            self._addLayer=ControlButton('Edit Layer')
            self._addLayer.value=self.__addEditedLayer

        else: 
            self._addLayer=ControlButton('add layer')
            self._addLayer.value=self.__addLayer
        

    def __setValuesFromDic(self, dic):
        for item in dic.items():
            if(item[0]!='constructor'):
                try:
                    exec(item[0]+'.value='+"'"+item[1]+"'")
                except:
                    exec(item[0]+'.value='+str(item[1]))
            
    
    def __addEditedLayer(self):
        l=self.__getConfig()
        dic=dict(l)
        self.parent.__addEditedLayer(dic)

    #\n e ir saltando
    #https://stackoverflow.com/questions/1325673/how-to-add-property-to-a-class-dynamically
    def translate(self, name,tipoJson):
        #print(tipoJson)
        s=name
        if(tipoJson[0]=='Integer'):
            m='self._'+s+'=ControlNumber('+"'"+s+"'"+')'
            exec(m)
            if(len(tipoJson)>1):
                m1='self._'+s+'.min= '+str(tipoJson[1])
                m2='self._'+s+'.max= '+str(tipoJson[2])
                exec(m1)
                exec(m2)               
            
        elif(tipoJson[0]=='Float'):
            m='self._'+s+'=ControlNumber('+"'"+s+"'"+')'
            exec(m)
            d='self._'+s+'.decimals=3'
            exec(d)
            if(len(tipoJson)>1):
                m1='self._'+s+'.min= '+str(tipoJson[1])
                m2='self._'+s+'.max= '+str(tipoJson[2])
                exec(m1)
                exec(m2)   
            
        
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

    def __getConfig(self):
        excepciones=['_parent_widget', '_mainmenu','_splitters','_tabs','_formset', '_formload','_formLoaded','_uid', '_addLayer', '']
        varAll=vars(self)
        lista=[]
        for var in varAll:
            if var.startswith("_") and var not in excepciones:
    
                m='lista.append(("self.'+var+'",self.'+var+'.value))'
                exec(m)

        #GUARDAR VALORES EN EL CONSTRUCTOR DEL DICCIONARIO
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

    def __loadSettings(self, lista):
        excepciones=['_parent_widget', '_mainmenu','_splitters','_tabs','_formset', '_formload','_formLoaded','_uid', '_addLayer']
        varAll=vars(self)
        #print(lista)
        for var in varAll:
            if var.startswith("_") and var not in excepciones:
                    a=lista.pop(0)
                    try:
                        m='self.'+var+'.value='+"'"+str(a)+"'"
                        exec(m)
                    except:
                        m='self.'+var+'.value='+str(a)
                        exec(m)  
        


    def __addLayer(self):
        l=self.__getConfig()
        dic=dict(l)

        #print(dic.items())
        #print(dic)
        #self.parent.__addLayerToModel(dic)
        self.parent.layers.append(dic)
        self.parent._layerCombo.add_item(dic['self._name'],dic)
        self.parent._layer.hide()
        #print(self.parent.layers)
