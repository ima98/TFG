from imports import *
import json

import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras import layers

from keras.models import Sequential
from keras.layers import Dense, Dropout


class layerFunctional(BaseWidget):
    def __init__(self, *args): 
        #args[0] layertype, args[1] father, args[2] optional dic
        BaseWidget.__init__(self,'keras layer')

        self.parent=args[1]

        self.topmost=True

        self.layerType=args[0]
        
        self._name=ControlText('name')
        if(len(args) > 2):
            t=args[2]
            self._name.readonly=True
            self._name.value=t['self._name']
            self.layerType=t['type']
        

        if(self.layerType=='Input from layers'):
            self._layerListToInput=ControlCheckBoxList('Generate input from layers')
            l=[]
            for x in self.parent.layerNames:
                l.append((x,False))

            self._layerListToInput.value=l

        else:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            with open(os.path.join(__location__,self.layerType+'.json')) as f:
                self.data= json.load(f)

            for key,value in self.data.items():
                self.translate(key, value)



            self._inputLayerSelect=ControlCombo('Input layer')

            prev=self.__getPreviousLayers()
            if prev==[]:
                self._inputLayerSelect.hide()
            else:
                for x in prev:
                            if x!=self._name.value:
                                self._inputLayerSelect.add_item(x)

        if(len(args) > 2):
            self.__setValuesFromDic(args[2])
            self._addLayer=ControlButton('Edit Layer')
            self._addLayer.value=self.__addEditedLayer

        else: 
            self._addLayer=ControlButton('add layer')
            self._addLayer.value=self.__addLayer
        

    def __setValuesFromDic(self, dic):
        #CAMBIAR ESTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        for item in dic.items():
            if(item[0]!='constructor' and item[0]!='input' and item[0]!='list' and item[0]!='type'):
                try:
                    exec(item[0]+'.value='+"'"+item[1]+"'")
                except:
                    exec(item[0]+'.value='+str(item[1]))
            elif(item[0]=='list'):
                l=item[1]
                prev=self.__getPreviousLayers()
                print('prev')
                print(prev)
                l2=[]
                if l is not None:
                    for x in prev:
                        if x==self._name.value:
                            print("hasta aqui")
                        else:
                            if x in l:
                                l2.append((x,True))
                            else:
                                l2.append((x,False))
                self._layerListToInput.value=l2
                

    def __getPreviousLayers(self):
        allLayers=self.parent.layerNames
        prev=[]
        i=0
        cond=True
        while cond==True and i<len(allLayers):
            if str(self._name.value)==str(allLayers[i]):
                print(self._name.value)
                print(allLayers[i])
                cond=False
                print(prev)
            else:
                prev.append(allLayers[i])
                i=i+1
        return prev
            
    
    def __addEditedLayer(self):
        l=self.__getConfig()
        dic=dict(l)
        self.parent._layer__addEditedLayer(dic)

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
        excepciones=['_parent_widget', '_mainmenu','_splitters','_tabs','_formset', '_formload','_formLoaded','_uid', '_addLayer', '', '_inputputLayerSelect', '_layerListToInput']
        varAll=vars(self)
        lista=[]
        for var in varAll:
            if var.startswith("_") and var not in excepciones:
    
                m='lista.append(("self.'+var+'",self.'+var+'.value))'
                exec(m)

        #GUARDAR VALORES EN EL CONSTRUCTOR DEL DICCIONARIO
        if(self.layerType!='Input from layers'):

            cons=self.data["constructor"]
            cons=cons[:-1]
            
            for tuplaLista in lista:
                if(tuplaLista[0]!="self._name" and tuplaLista[0]!="self._inputLayerSelect"):
                    name=tuplaLista[0][6:]
                    try:
                        cons=cons+name+"= '"+tuplaLista[1]+"', "
                    except:
                        cons=cons+name+"= "+str(tuplaLista[1])+", "
            
            cons=cons[:-2]
            cons=cons+")"
            lista.append(("constructor", cons))
            lista.append(("type", self.layerType))
            lista.append(("input", self._inputLayerSelect.value) )
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
        

    def __layerListToInputConfigGenerator(self):
        listaMetrics=self._layerListToInput.items
        l2=[]
        l2.append(("input", 'list'))
        l2.append(('self._name', self._name.value))
        l2.append(("type", self.layerType))
        l3=[]
        for x in listaMetrics:
            if x[1]==True:
                l3.append(x[0])
        l2.append(('list', l3))
        return l2
        

    def __addLayer(self):
        if(self.layerType!='Input from layers'):
            import errorManager
            l=self.__getConfig()
            dic=dict(l)
            if(dic['self._name'] not in self.parent.layerNames and dic['self._name']!=''):
                self.parent.layers.append(dic)
                self.parent._layerCombo.add_item(dic['self._name'],dic)
                self.parent._layer.hide() 
                self.parent.layerNames.append(dic['self._name'])
            else:
                errorManager.error(self, "Name already used by another layer", None)
        else:

            l=self.__layerListToInputConfigGenerator()
            dic=dict(l)
            print(dic)
            if(dic['self._name'] not in self.parent.layerNames and dic['self._name']!=''):
                self.parent.layers.append(dic)
                self.parent._layerCombo.add_item(dic['self._name'],dic)
                self.parent._layer.hide() 
                self.parent.layerNames.append(dic['self._name'])
            

