from datetime import datetime

from rest_framework.views import APIView
from rest_framework import status as https_status
from rest_framework.response import Response

from src.cases.managers import CaseManager
from src.cases.models import CaseModel
from src.cases.serializers import CaseSerializer


"""
Todos:
    1. Authentication
    2. Provide detail reasons for BadRequest
    3. add request format for each api
"""
class CaseView(APIView):
    @staticmethod
    def post(request):
        serializer = CaseSerializer(data=request.data)

        if serializer.is_valid():
            case = serializer.save()
            return Response(CaseSerializer(case).data, status=https_status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=https_status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get(request):
        try:
            case_id = request.query_params.get("case_id")
            model = CaseManager.get_by_case_id(case_id)
            return Response(CaseSerializer(model).data, status=https_status.HTTP_200_OK)
        except CaseModel.DoesNotExist:
            return Response({"error", "no such case"}, status=https_status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def patch(request):
        try:
            model = CaseManager.get_by_case_id(request.data.get("case_id"))
        except CaseModel.DoesNotExist:
            return Response({"error", "no such case"}, status=https_status.HTTP_400_BAD_REQUEST)
    
        serializer = CaseSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=https_status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=https_status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        try:
            model = CaseManager.get_by_case_id(request.data.get("case_id"))
            data = CaseSerializer(model).data
            model.delete()
            return Response(data, status=https_status.HTTP_204_NO_CONTENT)
        except CaseModel.DoesNotExist:
            return Response({"error", "no such case"}, status=https_status.HTTP_400_BAD_REQUEST)

class CaseListView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        qs = CaseModel.objects

        try:
            status = data.get("status") # str
            if status:
                qs = CaseManager.filter_by_status(status, qs)
            
            products = data.get("products") # str1,str2,...
            if products:
                qs = CaseManager.filter_by_products(products.split(","), qs)

            batch_nos = data.get("batch_nos") # str1,str2,...
            if batch_nos:
                qs = CaseManager.filter_by_batch_nos(batch_nos.split(","), qs)
            
            locations = data.get("locations") # str1,str2,...
            if locations:
                qs = CaseManager.filter_by_locations(locations.split(","), qs)
            
            issues = data.get("issues") # str1,str2,...
            if issues:
                qs = CaseManager.filter_by_issues(issues.split(","), qs)
            
            start_date = data.get("start_date") # yyyy-mm-dd
            end_date = data.get("end_date")
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            if end_date:
                end_date = datetime.fromisoformat(end_date)
            qs = CaseManager.filter_by_date_range(start=start_date, end=end_date, qs=qs)

            serializer = CaseSerializer(qs, many=True)
            return Response(data=serializer.data)

        except:
            data = {"error": "invalid filter arguments"}
            return Response(data=data, status=https_status.HTTP_400_BAD_REQUEST)
