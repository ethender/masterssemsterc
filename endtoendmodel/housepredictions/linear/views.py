from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import joblib
import numpy as np
import pandas as pd

# Create your views here.

def home(request):
    return render(request,'LinearPredictions.html')

def houseFeatures(request):
    posted_by = request.POST['postedby']
    underconstruction = request.POST['underconstruction']
    rera = request.POST['rera']
    bhkNo = request.POST['bhkno']
    bhkrk = request.POST['bhkorrk']
    readyToMove = request.POST['readytomove']
    resale = request.POST['resale']
    city = request.POST['city']
    rec = [posted_by,underconstruction,rera,bhkNo,bhkrk,readyToMove,resale]
    rec = pd.DataFrame(rec)
    print(f'''Posted: {posted_by},underconstruction:{underconstruction},RERA:{rera},BHKNO:{bhkNo},BhkRK:{bhkrk},Ready:{readyToMove},Resale:{resale},city:{city}''')

    return render(request,'results.html')

def encoding(record):
    return ''

def linearRegression(record):
    linmodel = joblib.load("/Users/ethender/Developer/python/mastersproject/endtoendmodel/savedmodel/linearregression.pkl")
    return''