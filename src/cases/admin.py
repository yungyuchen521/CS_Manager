from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe 
from src.cases.models import CaseModel, CaseResultModel

# Register your models here.
@admin.register(CaseModel)
class CaseAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "get_result"]

    def get_result(self, obj):
        return obj.case_result.id
        # return mark_safe('<a href="{}">{}</a>'.format(
        #     reverse("admin:auth_user_change", args=(obj.case_result.pk,)),
        #     obj.user.email
        # ))
    get_result.short_description = "result"
    
@admin.register(CaseResultModel)
class CaseResultAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "case", "result"]
