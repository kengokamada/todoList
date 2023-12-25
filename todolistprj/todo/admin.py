from django.contrib import admin
from . models import Task
from django.urls import path
# from .views import ExportCsvView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('admin/export-csv/', ExportCsvView.as_view(), name='admin_export-csv'),
# ]

# Register your models here.
admin.site.register(Task)