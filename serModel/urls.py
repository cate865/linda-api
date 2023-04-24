from django.urls import path, include
from .views import predict
 
urlpatterns = [ 
    path('predict', predict)
    
]