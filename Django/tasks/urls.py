
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_tasks, name='list_tasks'),
    path('add/<str:nombre>/<str:descripcion>/', views.add_task, name='add_task'),
    path('delete/<int:id_task>/', views.delete_task, name='delete_task'),
]
