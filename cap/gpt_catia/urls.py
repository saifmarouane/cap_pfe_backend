from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('home/', index_view, name='home'),
    path('bots/', bots_view, name='bots'),
    path('api/chat/', chat_view, name='chat'),
    path('apitest/', test_chat_api, name='c'),
    path('summary/', summary, name='c'),

    path('reinit/', reset_session_cookie, name='reinit'),
    # projet_django/urls.py





]
