from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", views.chat_ai, name="chat_ai"),
]