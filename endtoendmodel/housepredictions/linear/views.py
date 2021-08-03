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
import os

# Create your views here.

def home(request):
    return render(request,'LinearPredictions.html')

def houseFeatures(request):
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
    print(f'''Posted: {posted_by},underconstruction:{underconstruction},RERA:{rera},BHKNO:{bhkNo},BhkRK:{bhkrk},sqft:{sqft},Ready:{readyToMove},Resale:{resale},squareyard:{sqyard},city:{city}''')

    '''
        Loading Files
    '''
    pklFile = staticfiles_storage.path('RandomForestRegression.pkl')
    dataLoc = staticfiles_storage.path('train.csv')
    pandasData = pd.read_csv(dataLoc)
    mlModel = joblib.load(pklFile)

    '''
        Model preparing
    '''
    predctors = PredictorModel(pandasData,mlModel)
    #sqft = 545.1713396
    #sqyd = sqft / 9
    #record = [0, 0, 0, 1, 0, sqft, 1, 1, sqyd]'''
    result = predctors.getReport(rec,confidenceLevel=0.95,isTwoSided=True)
    result['predictedvalue'] = round(result['predictedvalue'][0],2)
    return render(request,'results.html',context=result)

