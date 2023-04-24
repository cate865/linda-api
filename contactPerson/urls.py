from django.urls import path, include
from .views import create_contact
 
urlpatterns = [ 
    path('contactperson/create', create_contact)
    
]