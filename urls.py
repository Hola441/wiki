from django.urls import path

from . import views

urlpatterns = [   
    path("", views.index, name="index"),
    path("create-new-page/", views.newPage, name="newPage"),   
    path("search/", views.searchResults, name="searchResults"),
    path("<str:page>/", views.pages, name="pages"),
    path("edit-page/<str:page>/", views.editPage, name="editPage"),
    path("save-page/<str:page>/", views.savePage, name="saveEditedPage"),
]
