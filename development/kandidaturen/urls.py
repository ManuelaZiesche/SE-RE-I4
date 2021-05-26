from django.urls import path
from . import views


app_name = 'kandidaturen'  # here for namespacing of urls.

urlpatterns = [
     path("", views.main_screen, name="homepage"),
     path("erstellen", views.kandidaturErstellenView, name="erstellenView"),
     path("erstellen/speichern", views.erstellen, name="erstellen"),

     path('ajax/laden', views.kandidatur_laden, name='kandidatur_laden'),
]
