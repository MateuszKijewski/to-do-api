from django.urls import path, include

from rest_framework.routers import DefaultRouter

from todo_api import views

router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet)
router.register('todo-list', views.TodoListViewset, base_name='todo-list')


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('quote/', views.InspirationalQuote.as_view()),
    path('todo-list/delete/', views.TaskListDelete.as_view()),
    path('', include(router.urls))
]
