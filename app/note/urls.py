from django.urls import path

from . import views


urlpatterns = [
    path('', views.note_list_create_view),
    path('<int:pk>/', views.note_delete_view),
    path('<int:pk>/update/', views.note_update_view),
    path('<int:pk>/delete/', views.note_delete_view),
    path('<str:tag>/tags/', views.note_filter_tags),
    #path('', views.note_mixins_view)
]
