from common import views
from django.urls import path, include

urlpatterns = [
    # City
    path('add/city/', views.CityAddView.as_view()),
    path('city/', views.CityGetAllView.as_view()),
    path('city/<int:pk>', views.CityGetView.as_view()),
    path('update/city/<int:pk>', views.CityUpdateView.as_view()),
    path('delete/city/<int:pk>', views.CityDeleteView.as_view()),
    # Industry
    path('add/industry/', views.IndustryAddView.as_view()),
    path('industry/', views.IndustryGetAllView.as_view()),
    path('industry/<int:pk>', views.IndustryGetView.as_view()),
    path('update/industry/<int:pk>', views.IndustryUpdateView.as_view()),
    path('delete/industry/<int:pk>', views.IndustryDeleteView.as_view()),
]