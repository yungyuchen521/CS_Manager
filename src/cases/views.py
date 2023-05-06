from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from src.cases.managers import CaseManager, TaskManager
from src.cases.models import CaseModel, TaskModel
from src.cases.serializers import CaseSerializer, TaskSerializer
from src.utils import ResponseHelper

INVALID_FILTER = "invalid filter arguments: {details}"


"""
Todos:
    1. Authentication
    2. Provide detail reasons for BadRequest
    3. add format hint for each api
"""
class CaseView(APIView):
    ITEM_NAME = "Case"

    @classmethod
    def post(cls, request):
        serializer = CaseSerializer(data=request.data)

        if serializer.is_valid():
            case = serializer.save()
            return Response(CaseSerializer(case).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def get(cls, request):
        case_id = request.query_params.get("case_id")

        try:    
            model = CaseManager.get_by_case_id(case_id)
        except CaseModel.DoesNotExist:
            return ResponseHelper.item_not_found_resp(item=cls.ITEM_NAME)

        return Response(CaseSerializer(model).data, status=status.HTTP_200_OK)

    @classmethod
    def patch(cls, request):
        try:
            model = CaseManager.get_by_case_id(request.data.get("case_id"))
        except CaseModel.DoesNotExist:
            return ResponseHelper.item_not_found_resp(item=cls.ITEM_NAME)
    
        serializer = CaseSerializer(model=model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete(cls, request):
        try:
            model = CaseManager.get_by_case_id(request.query_params.get("case_id"))
        except CaseModel.DoesNotExist:
            return ResponseHelper.item_not_found_resp(item=cls.ITEM_NAME)

        data = CaseSerializer(model).data
        model.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class CaseListView(APIView):
    @classmethod
    def post(cls, request):
        content_type = "application/json"

        invalid_resp = ResponseHelper.verify_content_type(
            expected_type=content_type,
            actual_type=request.content_type,
        )

        if invalid_resp:
            return invalid_resp

        data = request.data
        qs = CaseModel.objects

        try:
            stat = data.get("status") # str
            if stat:
                qs = CaseManager.filter_by_status(stat, qs)
            
            products = data.get("products") # List[str]
            if products:
                qs = CaseManager.filter_by_products(products, qs)

            batch_nos = data.get("batch_nos") # List[str]
            if batch_nos:
                qs = CaseManager.filter_by_batch_nos(batch_nos, qs)
            
            locations = data.get("locations") # List[str]
            if locations:
                qs = CaseManager.filter_by_locations(locations, qs)
            
            issues = data.get("issues") # List[str]
            if issues:
                qs = CaseManager.filter_by_issues(issues, qs)
            
            date_range = data.get("date_range", {})
            """
                {
                    start: yyyy-mm-dd,
                    end: yyyy-mm-dd,
                }
            """
            qs = CaseManager.filter_by_date_range(qs=qs, **date_range)

            serializer = CaseSerializer(qs, many=True)
            return Response(data=serializer.data)

        except Exception as e:
            return ResponseHelper.error_resp(
                msg=INVALID_FILTER,
                status_code=status.HTTP_400_BAD_REQUEST,
                details=str(e),
            )


class TaskView(APIView):
    ITEM_NAME = "Task"

    @classmethod
    def post(cls, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def patch(cls, request):
        """
            Todos:
                1. prevent changing case_id here
        """
        try:
            model = TaskManager.get_by_id(request.query_params.get("id"))
        except TaskModel.DoesNotExist:
            return ResponseHelper.item_not_found_resp(item=cls.ITEM_NAME)

        serializer = TaskSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            model.delete_img() # delete the original image
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete(cls, request):
        task_id = request.query_params.get("id")
        try:
            task = TaskManager.get_by_id(task_id)
        except TaskModel.DoesNotExist:
            return ResponseHelper.item_not_found_resp(item=cls.ITEM_NAME)
        
        data = TaskSerializer(task).data
        task.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
