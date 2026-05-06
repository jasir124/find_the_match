from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_view, name='search'),
    path('results/', views.results_view, name='results'),
]
