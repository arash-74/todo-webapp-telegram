from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from todo import views

app_name = 'todo'
urlpatterns = [
    path('todos/<str:chat_id>',csrf_exempt(views.Index),name='index'),
    path('todos/delete/<int:id>',views.remove_todo,name='delete'),
    path('todos/complete/<int:id>',views.complete_todo,name='complete'),
    path('todos/add/<str:chat_id>',csrf_exempt(views.add_todo),name='add'),
]