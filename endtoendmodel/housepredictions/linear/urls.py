from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('features',views.houseFeatures,name='features')
]