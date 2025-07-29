from django.contrib import admin
from .models import Task
# Register your models here.

class Taskadmin(admin.ModelAdmin):
    readonly_fields=("creationdate",)
    
admin.site.register(Task,Taskadmin)