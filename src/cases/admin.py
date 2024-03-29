from django.contrib import admin
from django.utils.html import format_html

from src.cases.models import CaseModel, TaskModel
from src.cases.managers import CaseManager, TaskManager
from src.cases.actions import analyze_cases, classify_tasks


@admin.register(CaseModel)
class CaseAdmin(admin.ModelAdmin):
    list_display = [
        "case_id",
        "status",
        "tasks",
        "created_at",
        "category",
        "report",
        "product_name",
        "batch_no",
        "location",
    ]
    list_editable = ["category", "report"]

    actions = ["analyze", "clear_analysis"]

    @staticmethod
    def tasks(obj):
        task_cnt = CaseManager.get_with_task_set_by_case_id(obj.case_id).task_set.count()
        url = f"http://127.0.0.1:8000/admin/cases/taskmodel/?q={obj.case_id}"
        return format_html(f"<a href={url}>{task_cnt}</a>")

    @admin.action(description="analyze and produce report")
    def analyze(self, request, queryset):
        analyze_cases(queryset)

        for case in queryset:
            self.message_user(request, f"<Case {case.case_id}> scheduled for analysis")

    @admin.action(description="clear anaylysis and report")
    def clear_analysis(self, request, queryset):
        tasks_affected = []

        for case in queryset:
            case.category = None
            case.report = None
            for task in case.task_set.all():
                task.category = None
                tasks_affected.append(task)

            self.message_user(request, f"<Case {case.case_id}> cleared")

        CaseManager.bulk_update(queryset, fields=["category", "report"])
        TaskManager.bulk_update(tasks_affected, fields=["category"])


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "case"]
    list_editable = ["category"]

    actions = ["predict"]

    search_fields = ["case__case_id"]

    @admin.action(description="classifies foreign matter in the image")
    def predict(self, request, queryset):
        classify_tasks(queryset)

        for task in queryset:
            self.message_user(request, f"<Task {task.id}> scheduled for image classification")
