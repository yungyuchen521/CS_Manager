from src.cases.models import CaseModel, TaskModel

from django.shortcuts import render, redirect
from .forms import CasesForm
from django.db import IntegrityError
from django.utils import timezone

from src.cases.actions import analyze_cases

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def result_view(request):
    if request.method == 'POST':
        pass
    else:
        pass
    
    today_cases = CaseModel.objects.filter(created_at__date=timezone.now())
    today_cases_dic = {}                    # 因為Django 的 html 不給用 [] 直接用 index 存取 list 所以要把圖片跟case對應上就用了字典
    for case in today_cases:
        if case.task_set.all().count() > 0:
            today_cases_dic[case.case_id] = case.task_set.all()
        else:
            today_cases_dic[case.case_id] = []

    # 更早以前的 case
    other_cases = CaseModel.objects.exclude(pk__in=today_cases).order_by('-created_at')
    other_cases_dic = {}       
    for case in other_cases:
        if case.task_set.all().count() > 0:
            other_cases_dic[case.case_id] = case.task_set.all()
        else:
            other_cases_dic[case.case_id] = []

    return render(request, 'cases/result.html',{
        'today_cases': today_cases,
        'today_cases_dic':today_cases_dic,
        'other_cases': other_cases,
        'other_cases_dic':other_cases_dic,
    })

def upload_view(request):

    if request.method == 'POST':
        caseform = CasesForm(request.POST, request.FILES)

        if caseform.is_valid():
            new_case = CaseModel(
                case_id=caseform.cleaned_data['case_id'], 
                status=caseform.cleaned_data['status'], 
                product_name=caseform.cleaned_data['product_name'], 
                batch_no=caseform.cleaned_data['batch_no'], 
                product_specs=caseform.cleaned_data['product_specs'] or None, 
                location=caseform.cleaned_data['location'] or None, 
                issue_details=caseform.cleaned_data['issue_details'] or None, 
                oem_feedback=caseform.cleaned_data['oem_feedback'] or None, 
                oem_status=caseform.cleaned_data['oem_status'] or None, 
                created_at=caseform.cleaned_data['created_at'], 
            )
            new_case.save()


            if caseform.cleaned_data.get('image1'):
                new_img = TaskModel(
                    img = caseform.cleaned_data['image1'],
                    case = new_case,
                )
                new_img.save()
            if caseform.cleaned_data.get('image2'):  
                new_img = TaskModel(
                    img = caseform.cleaned_data['image2'],
                    case = new_case,
                )
                new_img.save()
            if caseform.cleaned_data.get('image3'):
                new_img = TaskModel(
                    img = caseform.cleaned_data['image3'],
                    case = new_case,
                )
                new_img.save()

            # 清空上次的輸入框內容
            caseform.initial = {}
            caseform.data = {}
        else:
            errors = caseform.errors.as_text()
            print(" caseform.is_valid() fail ")
    else:
        caseform = CasesForm() 

    today_cases = CaseModel.objects.filter(created_at__date=timezone.now())

    # 因為Django 的 html 不給用 [] 直接用 index 存取 list 所以要把圖片跟case對應上就用了字典
    today_cases_dic = {}
    for case in today_cases:
        if case.task_set.all().count() > 0:
            today_cases_dic[case.case_id] = case.task_set.all()
        else:
            today_cases_dic[case.case_id] = []

    print(today_cases)
    return render(request, 'cases/upload.html',{
        'caseform' : caseform,
        'today_cases': today_cases,
        'today_cases_dic':today_cases_dic,
    })

# 更新資料庫現有資料
def update(request):
    if request.method == 'POST':
        try:
            case_id = request.POST.get('case_id')
            case = CaseModel.objects.get(case_id=case_id)

            status = request.POST.get('status')    # 選擇題
            product_name  = request.POST.get('product_name')
            batch_no = request.POST.get('batch_no')
            product_specs = request.POST.get('product_specs') or None
            location = request.POST.get('location') or None
            product_issue = request.POST.get('product_issue'),  # 選擇題
            issue_details = request.POST.get('issue_details') or None
            oem_feedback = request.POST.get('oem_feedback') or None
            oem_status = request.POST.get('oem_status') or None
            created_at = request.POST.get('created_at')
            category = request.POST.get("category")
            
            case.status = status
            case.product_name = product_name
            case.batch_no = batch_no
            case.product_specs = product_specs
            case.location = location
            case.product_issue = product_issue
            case.issue_details = issue_details
            case.oem_feedback = oem_feedback
            case.oem_status = oem_status
            case.created_at = created_at
            case.category = category
            case.save()
            print("更新成功")
        except IntegrityError as e:
            print("案例保存失败", str(e))

    return redirect('upload')


# 傳至網路分類
def classification(request):
    if request.method  == "POST":
        try:
            # 取出當天上傳的案例做分類
            today_cases = CaseModel.objects.filter(created_at__date=timezone.now())
            analyze_cases(today_cases)

        except IntegrityError as e:
                print("分類錯誤", str(e))

    return redirect('result')


def print_to_pdf(pdf, case, count):
    # 抓文字高度 620~750 約 130，再加上圖片高度 50 好了 => 一個案子高度為 220

    # 1. 左邊那排的細節資料
    pdf.drawString(50, 750-220*count, "case id: "+ str(case.case_id)) # 參數:(x,y)
    pdf.drawString(50, 735-220*count, "status: "+ case.status) 
    pdf.drawString(50, 720-220*count, "product name: "+ case.product_name) 
    pdf.drawString(50, 705-220*count, "batch number: "+ str(case.batch_no)) 
    if case.product_specs:
        pdf.drawString(50, 690-220*count, "product specs: "+ case.product_specs)
    else:
        pdf.drawString(50, 690-220*count, "product specs: "+ "No info")
    if case.location:
        pdf.drawString(50, 675-220*count, "location: "+ case.location)
    else:
        pdf.drawString(50, 675-220*count, "location: "+ "No info")
    if case.product_issue:
        pdf.drawString(50, 660-220*count, "product_issue: "+ case.product_issue)
    else:
        pdf.drawString(50, 660-220*count, "product_issue: "+ "No info")
    pdf.drawString(50, 645-220*count, "created time: "+ case.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    if case.category:
        pdf.drawString(50, 630-220*count, "category: "+ case.category)
    else:
        pdf.drawString(50, 630-220*count, "category: None")


    #  2. 右邊那排的較大的資料
    if case.issue_details:
        pdf.drawString(270, 750-220*count, "Customer Complaint Details: "+ case.issue_details)
    else:
        pdf.drawString(270, 750-220*count, "Customer Complaint Details: "+ "No info")
    if case.oem_feedback:
        pdf.drawString(270, 700-220*count, "original factory feedback: "+ case.oem_feedback)
    else:
        pdf.drawString(270, 700-220*count, "original factory feedback: "+ "No info")
    if case.oem_status:
        pdf.drawString(270, 660-220*count, "original factory feedback status: "+ case.oem_status)
    else:
        pdf.drawString(270, 660-220*count, "original factory feedback status: "+ "No info")
    
    # 3. 圖片
    if case.task_set.all().count() > 0:
        x_count = 0
        for task in case.task_set.all():
            image_path = task.img.path
            pdf.drawImage(image_path, 50 + 70 * x_count, 570 -220*count, 50, 50) # 給的是 (圖片左下角的 x 坐標, 圖片左下角的 y 坐標)
            x_count += 1
    else:
        pdf.drawString(240, 600-220*count, "No image for this case")

    # 4. 最後印個分隔線
    line = "------------------------------------------------------------------------------------------------------------"
    pdf.drawString(50, 565 -220*count, line)
         

def export_to_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    filename = timezone.now().strftime("%Y_%m_%d") + '.pdf'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    pdf = canvas.Canvas(response)
    pdf.setTitle(timezone.now().strftime("%Y-%m-%d") + " Report")

    width, height = letter
    # print(f"PDF 寬度:{width}, PDF 高度, {height}") # 單位: point， 寬: 612.0，高: 792.0

    
    # 在指定位置繪製 data，data 必須為 str 或數字
    # 原點是 PDF 左下角，往右X軸增加、往上Y軸增加
    today_cases = CaseModel.objects.filter(created_at__date=timezone.now())
    pdf.setFont("Helvetica", 20)  # 設置文字大小為 20
    pdf.drawString( 50 , height, "Today's Report")

    pdf.setFont("Helvetica", 12)
    count = 0 
    for i in range(len(today_cases)):
        case = today_cases[i]
        print_to_pdf(pdf, case, count)

        # 檢查是否需要換頁
        count +=1 
        if count  == 3:
            count = 0
            pdf.showPage()
    
    # 今日案例跟批次檢查中間強制換頁
    if len(today_cases) % 3 != 0:
        pdf.showPage()

    # 檢查有沒有同一個批次出現 2 個以上案例就要特別點出，並提供這個批次的所有案例的資料
    distinct_batches = CaseModel.objects.values('batch_no').distinct()
    batch_values = [batch['batch_no'] for batch in distinct_batches]
    flag = 0
    for batch in batch_values:
        instances = CaseModel.objects.filter(batch_no=batch)
        if len(instances) >= 2:
            flag = 1
            break
    
    if flag == 1:
        for batch_value in batch_values:
            count = 0
            cases = CaseModel.objects.filter(batch_no=batch_value)
            if len(cases) >= 2:
                pdf.setFont("Helvetica", 20)  # 設置文字大小為 20
                pdf.drawString(50, height, "Batch Worning for batch " +  batch_value)
                pdf.setFont("Helvetica", 12) 
                for case in cases:
                    print_to_pdf(pdf, case, count)
                    # 檢查是否需要換頁
                    count +=1 
                    if count  == 3:
                        count = 0
                        pdf.showPage()

                if len(cases) > 3 and count != 0:
                    pdf.showPage()



            



    pdf.showPage()
    pdf.save()


    return response
