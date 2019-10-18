from django.contrib import admin

from todo_api import models


admin.site.register(models.QuoteGroup)
admin.site.register(models.TodoTask)
admin.site.register(models.UserProfile)
admin.site.register(models.TodoTaskList)