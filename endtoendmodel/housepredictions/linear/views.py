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

    return render(request,'results.html')

def encoding(record):
    return ''

def linearRegression(record):
    linmodel =
    return''