from django.contrib import admin
from src.cases.models import CaseModel, TaskModel

# Register your models here.
@admin.register(CaseModel)
class CaseAdmin(admin.ModelAdmin):
    list_display = ["case_id", "product_name", "batch_no", "created_at"]
    
@admin.register(TaskModel)
class CaseResultAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "result", "case"]
