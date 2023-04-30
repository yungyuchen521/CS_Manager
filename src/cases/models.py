from django.db import models

from src.cases.define import (
    CASE_STATUS_CHOICES,
    CASE_STATUS_PENDING,
    TASK_RESULT_CHOICES,
)


class CaseModel(models.Model):
    class Meta:
        db_table = "case"

    id = models.AutoField(primary_key=True)
    case_id = models.CharField(max_length=16)

    status = models.CharField(
        max_length=16,
        choices=CASE_STATUS_CHOICES,
        default=CASE_STATUS_PENDING,
    )
    product_name = models.CharField(max_length=16)
    batch_no = models.CharField(max_length=16)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)


class TaskModel(models.Model):
    class Meta:
        db_table = "task"

    id = models.AutoField(primary_key=True)

    img = models.ImageField(upload_to="tasks/")
    category = models.CharField(
        max_length=32,
        choices=TASK_RESULT_CHOICES,
        blank=True,
        null=True,
    )
    result = models.TextField(
        blank=True,
        null=True,
    )

    case = models.ForeignKey(
        to=CaseModel,
        on_delete=models.CASCADE,
        related_name="task_set",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
