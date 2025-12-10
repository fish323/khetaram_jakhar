from django.urls import path
from .import views

urlpatterns = [
    path('contactusview',views.contactusview,name = 'contactview'),
]