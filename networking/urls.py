
from django.urls import path, include
from . import views

urlpatterns = [
    path('networks/', views.NetworkList.as_view()),
    path('networks/<int:pk>/', views.NetworkDetailView.as_view())
]
