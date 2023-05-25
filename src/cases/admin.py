from django.contrib import admin

from src.cases.models import CaseModel, TaskModel
from src.cases.actions import classify_images


@admin.register(CaseModel)
class CaseAdmin(admin.ModelAdmin):
    list_display = [
        "case_id",
        "status",
        "product_name",
        "batch_no",
        "location",
        "created_at",
    ]
    
@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "result", "case"]
    list_editable = ["category"]

    actions = ["predict"]

    @admin.action(description="classifies foreign matter in the image")
    def predict(self, request, queryset):
        classify_images(queryset)
        
        for task in queryset:
            self.message_user(request, f"<Task {task.id}> scheduled for image classification")
