from django.urls import path, include;
from . import views

urlpatterns = [
    path('', views.api_random_notes),
    path('notes/', include('note.urls'))
]
