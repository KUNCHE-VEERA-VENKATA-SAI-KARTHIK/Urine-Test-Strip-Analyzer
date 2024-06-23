
from django.urls import path,include
from .views import TextImageAPI

urlpatterns = [
    path('', TextImageAPI.as_view()),
]