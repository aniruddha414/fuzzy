from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stored', views.stored, name='stored'),
    path('viewrules', views.viewrules, name='viewrules'),
    path('feedrules', views.feedrules, name='feedrules'),
    path('deleterule', views.deleterule, name='deleterule'),
    path('populate', views.populate, name='populate'),
]