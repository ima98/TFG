from imports import *
import sklearn
import json
from PyQt5.QtWidgets import QMessageBox

def fileGeneratorSequentialModel(stringList, fileName, compileList, fitList):
        with open('imports.py', 'r') as file:
            imports = file.read()
        fname='generated.py'
        with open(fname, 'w') as f:
            f.write(imports)
            f.write('\n')
            f.write("from numpy import loadtxt")
            f.write('\n')
            f.write("import tensorflow as tf")
            f.write('\n')
            f.write("from keras.models import Sequential")
            f.write('\n')
            

            f.write("dataset = loadtxt("+"'"+fileName+"'"+", delimiter=',')")
            f.write('\n')
            f.write("X = dataset[:,0:dataset.shape[1]-1] \n")
            f.write("y = dataset[:,dataset.shape[1]-1] \n")
            f.write("model = Sequential()")
            f.write('\n')

            for x in stringList:
                f.write(x)
                f.write("\n")
                f.write("model.add(layerTemp)\n")


            #COMPILER PART
            metrics=""
            for index, item in enumerate(compileList[3]):
                if index != len(compileList[3]) - 1:
                    #print(item, 'is NOT last in the list ✅')
                    metrics=metrics+"'"+item+"',"
                else:
                    #print(item, 'is last in the list ❌')
                    metrics=metrics+"'"+item+"'"

            f.write("model.compile(optimizer='"+compileList[0]+"', loss='"+compileList[1]+"', steps_per_execution=int("+str(compileList[2])+"), metrics=["+metrics+"])\n")
           

            #FIT
            f.write("model.fit(X, y, epochs=int("+str(fitList[0])+"), batch_size=int("+str(fitList[1])+"), verbose=int("+fitList[2]+"), validation_split="+fitList[3]+")")
            f.write("\n")
            
            f.write("model.summary()")
            f.close()


def fileGeneratorSKlearn(fileName,train_test_splitList, constructor):
        with open('imports.py', 'r') as file:
            imports = file.read()
        fname='generated.py'
        with open(fname, 'w') as f:
            f.write(imports)
            f.write('\n')

            f.write('#LOADING DATA\n')
            f.write('from pandas import read_csv \n')
            f.write("inputData = read_csv("+"'"+fileName+"'"+", delimiter=',', header=1) \n")
            f.write("y = inputData.iloc[:,inputData.shape[1]-1] \n")
            f.write('X=inputData.iloc[:, 0:inputData.shape[1]-2] \n')

            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('#DATA SPLIT \n')
            f.write("X_train,X_test,y_train,y_test=train_test_split(X,y,test_size="+str(train_test_splitList[0])+", random_state=int("+str(train_test_splitList[1])+"), shuffle="+str(train_test_splitList[2])+")\n")

            f.write("modelo="+constructor+"\n")

            f.write("modelo.fit(X_train,y_train)\n")
            