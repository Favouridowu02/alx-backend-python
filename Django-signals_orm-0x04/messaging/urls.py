from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('<int:pk>/history/', views.message_history, name='message_history'),
]
