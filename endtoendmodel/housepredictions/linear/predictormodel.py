import numpy as np
import pandas as pd
import joblib
import copy
from sklearn.preprocessing import LabelEncoder



class PredictorModel:



    def __init__(self):
        self.model = ''
        self.data = []
        self.transformedData = []
        self.pkl = '/Users/ethender/Developer/python/mastersproject/endtoendmodel/savedmodel/linearregression.pkl'
        self.dataLoc = '/Users/ethender/Developer/python/mastersproject/data/prices/train.csv'
        self.loadData()
        self.loadModel()

    def loadModel(self):
        self.model = joblib.load(self.pkl)

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




if __name__ == "__main__":
    predictor = PredictorModel()
    sqft = 545.1713396
    sqyd = sqft/9
    record = [0,0,0,1,0,sqft,1,1,sqyd]
    print(predictor.predictModel(record))