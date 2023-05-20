from django import forms
from .models import TaskModel
from src.cases.define import (
    CASE_STATUS_CHOICES,
    CASE_STATUS_PENDING,
    TASK_RESULT_CHOICES,
    PRODUCT_ISSUE_CHOICES,
)


class CasesForm(forms.Form):
    cases_id = forms.CharField(max_length=16, label="個案號碼", required=True, 
                                widget=forms.TextInput(attrs={'class': 'myinput'}),)
    status = forms.ChoiceField(choices=CASE_STATUS_CHOICES, label="狀態", required=True)

    product_name = forms.CharField(max_length=16, label="產品名稱", required=True,
                                    widget=forms.TextInput(attrs={'class': 'myinput'}))
    batch_no = forms.CharField(max_length=16, label="產品批號", required=True,
                               widget=forms.TextInput(attrs={'class': 'myinput'}),)
    product_specs = forms.CharField(max_length=16, label="產品規格", 
                                    widget=forms.TextInput(attrs={'class': 'myinput'}),)

    location = forms.CharField(max_length=32, label="地名", 
                               widget=forms.TextInput(attrs={'class': 'myinput'}),)
    product_issue = forms.ChoiceField(
        choices= PRODUCT_ISSUE_CHOICES,
        label= "產品問題"
    )

    issue_details = forms.CharField(label = "客訴詳細資訊", widget=forms.Textarea(attrs={'class': 'textinput'}))

    oem_feedback = forms.CharField(label="原廠 feedback ", widget=forms.Textarea(attrs={'class': 'textinput'}))
    oem_status = forms.CharField(label="原廠 feedback Status", widget=forms.Textarea(attrs={'class': 'textinput'}))
    created_at = forms.DateTimeField(label="立案時間", required=True)


    image1 = forms.ImageField(required=False, label="image1")
    image2 = forms.ImageField(required=False, label="image2")
    image3 = forms.ImageField(required=False, label="image3")
