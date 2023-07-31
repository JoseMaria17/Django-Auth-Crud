from django.contrib import admin
from .models import Task

# aqui se crea un campo en la tabla task de solo lectura
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Aqui agregamos las tablas al panel de administracion
admin.site.register(Task, TaskAdmin)
