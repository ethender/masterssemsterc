from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import joblib
import numpy as np
#from predictormodel import PredictorModel
from linear.predictormodel import PredictorModel
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd
import warnings
import os

# Create your views here.

def home(request):
    warnings.filterwarnings("ignore")
    return render(request,'LinearPredictions.html')

def houseFeatures(request):
    warnings.filterwarnings("ignore")
    posted_by = request.POST['postedby']
    underconstruction = int(request.POST['underconstruction'])
    rera = int(request.POST['rera'])
    bhkNo = int(request.POST['bhkno'])
    bhkrk = int(request.POST['bhkorrk'])
    sqft = float(request.POST['sqft'])
    sqyard = sqft/9
    readyToMove = int(request.POST['readytomove'])
    resale = int(request.POST['resale'])
    city = request.POST['city']
    rec = [posted_by,underconstruction,rera,bhkNo,bhkrk,sqft,readyToMove,resale,sqyard]
    #print(f'''Posted: {posted_by},underconstruction:{underconstruction},RERA:{rera},BHKNO:{bhkNo},BhkRK:{bhkrk},sqft:{sqft},Ready:{readyToMove},Resale:{resale},squareyard:{sqyard},city:{city}''')

    '''
        Loading Files
    '''
    rfrPklFile = staticfiles_storage.path('RandomForestRegression.pkl')
    etrPklFile = staticfiles_storage.path('extratreesregressor.pkl')
    dtrPklFile = staticfiles_storage.path('DecisionTreeRegressor.pkl')
    gbrPklFile = staticfiles_storage.path('gradientbosstingregressor.pkl')

    dataLoc = staticfiles_storage.path('train.csv')
    pandasData = pd.read_csv(dataLoc)
    #mlModel = joblib.load(pklFile)
    rfrModel = joblib.load(rfrPklFile)
    etrModel = joblib.load(etrPklFile)
    dtrModel = joblib.load(dtrPklFile)
    gbrModel = joblib.load(gbrPklFile)

    models = {'RandomForest':rfrModel,'ExtraTrees':etrModel,'DecisionTrees':dtrModel,'GradientBoosting':gbrModel}

    '''
        Model preparing
    '''
    predctors = PredictorModel(pandasData,models)
    result = predctors.getReport(rec,confidenceLevel=0.95,isTwoSided=True)
    result['predictedvalue'] = round(result['predictedvalue'][0],2)
    result['modelsreport'] = predctors.getAllModelsReport(rec)
    result['similardata'] = predctors.getCitySimilarPrices(city)
    return render(request,'results2.html',context=result)

