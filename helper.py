def getDataSet(filePath):
    from scipy.io import arff
    from pandas import read_csv
    import pandas as pd

    if(filePath.endswith(".arff")):
        dataL = arff.loadarff(filePath)
        inputData = pd.DataFrame(dataL[0])
    else:
        inputData = read_csv(filePath, delimiter=',', header=1)

    for dtype in inputData.dtypes.iteritems():
        if (dtype[1]=='O'):
            inputData[dtype[0]],_=pd.factorize(inputData[dtype[0]])

    y = inputData.iloc[:,inputData.shape[1]-1] 
    X=inputData.iloc[:, 0:inputData.shape[1]-2] 


    return X,y,inputData