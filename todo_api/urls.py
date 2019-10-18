from django.urls import path, include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from todo_api import views

router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet)
router.register('todo-list', views.TodoListViewset, base_name='todo-list')
router.register(r'todo-list/(?P<list_id>.+)/tasks', views.TodoTaskViewset, base_name='tasks')

app_name = 'todo_api'

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('quote/', views.InspirationalQuote.as_view()),
    path('todo-list/delete/', views.TaskListDelete.as_view()),
    url(r'^test/(?P<info>.+)/$', views.TestViewset.as_view()),
    url(r'^', include(router.urls))
]
