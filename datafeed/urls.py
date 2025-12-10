from django.urls import path
from . import views

urlpatterns = [
    path('workexpview', views.workexpview, name='workexpview'),
    path('equipmentview', views.equipmentview, name='equipmentview'),
    path('strengthview', views.strengthview, name='strengthview'),
    
    # Reorder URLs
    path('reorder_equipment/', views.reorder_equipment, name='reorder_equipment'),
    path('reorder_work/', views.reorder_work, name='reorder_work'),
    path('reorder_strength/', views.reorder_strength, name='reorder_strength'),
]