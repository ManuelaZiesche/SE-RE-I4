from django.urls import path
from . import views


app_name = 'kandidaturen'  # here for namespacing of urls.

urlpatterns = [
     path("", views.main_screen, name="homepage"),
]
