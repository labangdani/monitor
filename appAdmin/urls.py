from django.urls import path 
from .views import *


urlpatterns = [
    path("",liste_objects, name="liste"),
    path('ping/', ping_url),
    path("export", download_excel_data, name="export_excel"),
    path("actif", actif_list, name="actif-list"),
    path("non_actif", non_actif_list, name="non_actif_list"),
    path("search/", search, name="search"),
    path('create_link/', create_form, name="create_form"),

    
]