from django.urls import path
from .import views

urlpatterns = [
    path('',views.baseview, name = 'baseview'),
    path('homeview',views.homeview, name = 'homeview'),
    path('aboutusview',views.aboutusview, name = 'aboutusview'),
    path('photosview',views.photosview, name = 'photosview'),
]