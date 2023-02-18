from django.urls import path
from .views import TaskList, TaskDetail, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskLoginView, TaskRegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', TaskLoginView.as_view(), name='login'),
    path('register/', TaskRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='list'), name='logout'),
    path('', TaskList.as_view(), name='list'),
    path('task/<int:pk>/',TaskDetail.as_view(), name='details'),
    path('create-task/', TaskCreateView.as_view(), name='create'),
    path('update-task/<int:pk>/',TaskUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/',TaskDeleteView.as_view(), name='delete'),
]
