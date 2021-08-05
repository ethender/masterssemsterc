import numpy as np
import pandas as pd
import joblib
import copy
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import VotingRegressor
from sklearn.model_selection import train_test_split
from scipy import stats
import warnings
import os
from django.conf import Settings



class PredictorModel:

    def __init__(self,panadasData,models):
        warnings.filterwarnings("ignore")
        self.model = ""
        self.models = models
        self.data = panadasData
        self.transformedData = []
        self.convertDataPandas()
        self.combineAllModels()
        '''print(self.data.head())
        print('-'*50)
        print(self.transformedData.head())'''

    '''def __init__(self):
        self.model = ''
        self.data = []
        self.transformedData = []
        #self.pkl = '../static/savedmodel/RandomForestRegression.pkl'

        #self.dataLoc = '../static/data/prices/train.csv'
        self.loadData()
        self.loadModel()'''

    '''def loadModel(self):
        self.model = joblib.load(self.pkl)'''

    def combineAllModels(self):
        modelsList = []
        for name, model in self.models.items():
            modelsList.append((name,model))
        self.model = VotingRegressor(modelsList)
        x = self.transformedData.iloc[:,:-1]
        y = self.transformedData.iloc[:,-1]
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3)
        self.model.fit(x_train,y_train)

    def convertDataPandas(self):
        self.data['STATE_OR_CITY'] = self.getCities()
        self.data['SQUARE_YARD'] = self.convertSquareYard()
        self.data['TARGET_AMOUNT'] = self.convertTargetinLakhs()
        self.transformData()

    def loadData(self):
        self.data = pd.read_csv(self.dataLoc)
        self.data['STATE_OR_CITY'] = self.getCities()
        self.data['SQUARE_YARD'] = self.convertSquareYard()
        self.data['TARGET_AMOUNT'] = self.convertTargetinLakhs()
        self.transformData()


    def getCities(self):
        state = []
        for addr in self.data['ADDRESS']:
            state.append(addr.split(',')[1])
        return state

    def convertSquareYard(self):
        return self.data['SQUARE_FT']/9

    def convertTargetinLakhs(self):
        return self.data['TARGET(PRICE_IN_LACS)']*100000


    def transformData(self):
        self.transformedData = copy.deepcopy(self.data)
        prepareData = pd.concat([self.transformedData.iloc[:,:8],self.transformedData.iloc[:,12:]],axis=1)
        del prepareData['STATE_OR_CITY']
        postedEncoder = LabelEncoder()
        bhkorrkEncoder = LabelEncoder()
        prepareData['POSTED_BY'] = postedEncoder.fit_transform(prepareData['POSTED_BY'])
        prepareData['BHK_OR_RK'] = bhkorrkEncoder.fit_transform(prepareData['BHK_OR_RK'])
        self.transformedData = prepareData

    def predictModel(self,record):
        return self.model.predict([record])

    def confidenceInterval(self,predictedVal,confidenceLevel=0.95,isTwoSided=True):
        std = round(np.std(self.data['TARGET_AMOUNT']),2)
        lenOfData = len(self.data['TARGET_AMOUNT'])
        standardError = std/np.sqrt(lenOfData)
        alpha = 1-confidenceLevel
        if isTwoSided:
            alpha = alpha/2
        degreesOfFreedom = lenOfData-1
        tvalue = round(stats.t.ppf(alpha,degreesOfFreedom),2)
        minusValue = predictedVal-tvalue*standardError
        plusValue = predictedVal+tvalue*standardError
        values = (round(minusValue[0],2),round(plusValue[0],2))
        return values

    def getReport(self,record,confidenceLevel=0.95,isTwoSided=True):
        predict = self.predictModel(record)
        interval = self.confidenceInterval(predict,confidenceLevel,isTwoSided)
        return {'predictedvalue':predict,'confidence':interval}

    def getAllModelsReport(self,record):
        report = {}
        for name,model in self.models.items():
            predict = model.predict([record])
            conf = self.confidenceInterval(predict)
            report[name] = {'predictedvalue':predict,'confidence':conf}
        return report

    def getCitySimilarPrices(self,cityOrDistrict):
        data = copy.deepcopy(self.data)
        data['STATE_OR_CITY'] =  data['STATE_OR_CITY'].str.lower()
        return data[data['STATE_OR_CITY'] == cityOrDistrict.lower()].to_json(orient='index')

'''if __name__ == "__main__":
    predictor = PredictorModel()
    sqft = 545.1713396
    sqyd = sqft/9
    record = [0,0,0,1,0,sqft,1,1,sqyd]
    predictedValue = predictor.predictModel(record)
    print(predictedValue[0])
    print(predictor.confidenceInterval(predictedValue,0.95))
'''