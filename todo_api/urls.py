from django.urls import path, include

from rest_framework.routers import DefaultRouter

from todo_api import views

router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet)
router.register('todo-list', views.TodoTaskViewset, base_name='todo-list')


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('todo-list/delete/', views.TaskDeleteApiView.as_view()),
    path('', include(router.urls))
]
