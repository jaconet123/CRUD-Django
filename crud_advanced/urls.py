
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('logout/', views.logoutx, name="logoutx"),
    path('login/', views.loginx, name="loginx"),
    path('create_task/', views.create_task, name="createtask"),
    path('task_detail/<int:task_id>', views.task_detail, name="taskdetail"),
    path('task_detail/<int:task_id>/complete', views.complete_task, name="completetask"),
    path('task_detail/<int:task_id>/delete', views.delete_task, name="deletetask"),




]
# 1:22:07
