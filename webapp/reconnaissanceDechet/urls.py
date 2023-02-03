from django.urls import path
from . import views

urlpatterns = [
    path('', views.reconnaissanceDechet, name='reconnaissanceDechet'),
    path('resultatReconnaissanceDechet/', views.resultatReconnaissanceDechet, name='resultatReconnaissanceDechet'),
    path('ajoutPointMap/', views.ajoutPointMap, name='ajoutPointMap'),
    path('confirmationAjoutPointMap/', views.confirmationAjoutPointMap, name='confirmationAjoutPointMap'),
    path('map/', views.map, name='map'),    
]