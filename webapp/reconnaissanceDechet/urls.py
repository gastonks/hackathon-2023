from django.urls import path
from . import views

urlpatterns = [
    path('', views.reconnaissanceDechet, name='reconnaissanceDechet'),
    path('', views.resultatReconnaissanceDechet, name='resultatReconnaissanceDechet'),
]