import os

from django.conf import settings
from django.db import models

from src.cases.define import (
    CASE_STATUS_CHOICES,
    CASE_STATUS_PENDING,
    TASK_RESULT_CHOICES,
    PRODUCT_ISSUE_CHOICES,
)


class CaseModel(models.Model):
    class Meta:
        db_table = "case"

    id = models.AutoField(primary_key=True)
    case_id = models.CharField(max_length=16, unique=True) # 個案號碼

    status = models.CharField(
        max_length=16,
        choices=CASE_STATUS_CHOICES,
        default=CASE_STATUS_PENDING,
    ) # 狀態

    product_name = models.CharField(max_length=16) # 產品名稱
    batch_no = models.CharField(max_length=16) # 產品批號
    product_specs = models.CharField(max_length=16, null=True, blank=True) # 產品規格

    location = models.CharField(max_length=32, null=True, blank=True) # 地名 (產品規格右邊)

    product_issue = models.CharField(
        max_length=16,
        choices=PRODUCT_ISSUE_CHOICES, # choices 代表只能從裡面挑一個
        null=True,
        blank=True,
    ) # 產品問題
    issue_details = models.TextField(null=True, blank=True) # 客訴詳細資訊

    oem_feedback = models.TextField(null=True, blank=True) # 原廠 feedback 
    oem_status = models.TextField(null=True, blank=True) # 原廠 feedback Status

    created_at = models.DateTimeField() # 立案日期 (auto_now_add should be True in Prod)
    updated_at = models.DateTimeField(auto_now=True, editable=False, )


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


    def delete(self, *args, **kwargs):
        self.delete_img()
        super().delete(*args, **kwargs)

    def delete_img(self):
        if settings.DEBUG:
            file_path = settings.MEDIA_ROOT.parent / self.img.path
            os.remove(file_path)
        else:
            raise NotImplementedError
