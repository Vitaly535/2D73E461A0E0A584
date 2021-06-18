from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.sign_up, name="signup"),
    path('', views.index, name='index'),
    path('task/<str:task_id>', views.get_status, name='status'),
]
