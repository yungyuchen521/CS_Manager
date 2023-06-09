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
"""
class CaseView(APIView):
    ITEM_NAME = "Case"

    @classmethod
    def post(cls, request):
        # Create a new `Case`

        """
        ===== request format =====
            body:
                {
                    *case_id: string
                    *product_name: string
                    *batch_no: string
                    *created_at: yyyy-mm-dd
                }

            query parameters:
                NA
            
        ===== response format =====
            {
                all info of the newly created `Case`
            }
        """
        serializer = CaseSerializer(data=request.data)

        if serializer.is_valid():
            case = serializer.save()
            return Response(CaseSerializer(case).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def get(cls, request):
        # Get an existing `Case`

        """
        Todos:
            1. respond with the encoded image instead of file path
            
        ===== request format =====
            body:
                NA
            query parameters:
                *case_id: string
            
        ===== response format =====
            {
                case: {
                    all info of the case
                },
                task_set: [
                    // all corresponding `Task`s

                    {
                        all info of task 1
                    },
                    {
                        all info of task 2
                    },
                    ...
                ]
            }
        """

        case_id = request.query_params.get("case_id")

        try:
            case_model = CaseManager.get_with_task_set_by_case_id(case_id)
        except CaseModel.DoesNotExist:
            return ResponseHelper.item_not_found_resp(item=cls.ITEM_NAME)

        data = {
            "case": CaseSerializer(case_model).data,
            "task_set": [
                TaskSerializer(task_model).data
                for task_model in case_model.task_set.all()
            ]
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @classmethod
    def patch(cls, request):
        # Update an existing `Case`

        """
        ===== request format =====
            body:
                anything you want to edit (except updated_at & id)
                
                e.g.
                {
                    batch_no: 12345678,
                    product_name: blablabla,
                    ...
                }
            
            query parameters:
                *case_id: string
            
        ===== response format =====
            {
                all info of the updated `Case`
            }
        """
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
        # Delete an existing `Case`

        """
        ===== request format =====
            body:
                NA
            
            query parameters:
                *case_id: string
            
        ===== response format =====
            {
                all info of the deleted `Case`
            }
        """
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
        # Filter & return`Case`s 

        """
        ===== request format =====
            body:
                filter criteria

                e.g.
                {   
                    status: [RESOLVED]
                    products: [PGSG, SMAG],
                    date_range: {
                        start: yyyy-mm-dd
                    }
                }
                -> return all 'Case's whose
                    `status` == RESOLVED &&
                    `product` in {PGSG, SMAG} &&
                    `created_at` >= yyyy-mm-dd 

            query parameters:
                NA

        ===== response format =====
            {
                all info of case 1
            },
            {
                all info of case 2
            },
            ...

            p.s. info of corresponding `Task`s is not returned
        """

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
        # Create a new `Task` & assign it to an existing `Case`

        """
        ===== request format =====
            please refer to api_samples/tasks/post.py
            
        ===== response format =====
            {
                all info of the newly created `Task`
            }
        """

        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def patch(cls, request):
        # Update an existing `Task`

        """
        Todos:
            1. prevent changing case_id here
        
        ===== request format =====
            body:
                please refer to api_samples/tasks/patch.py
            
            query parameters:
                *id: string
            
        ===== response format =====
            {
                all info of the updated `Task`
            }
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
        # Delete an existing `Task`

        """
        ===== request format =====
            body:
                NA
            
            query parameters:
                *id: string
            
        ===== response format =====
            {
                all info of the deleted `Task`
            }
        """

        task_id = request.query_params.get("id")
        try:
            task = TaskManager.get_by_id(task_id)
        except TaskModel.DoesNotExist:
            return ResponseHelper.item_not_found_resp(item=cls.ITEM_NAME)
        
        data = TaskSerializer(task).data
        task.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
