from typing import Iterable, List, Optional

from django.db.models import QuerySet

from src.cases.models import CaseModel, TaskModel
from src.utils import DatetimeHelper


class CaseManager:
    @staticmethod
    def get_by_case_id(case_id: str):
        return CaseModel.objects.get(case_id=case_id)

    @staticmethod
    def get_with_task_set_by_case_id(case_id: str):
        return (
            CaseModel.objects
            .prefetch_related("task_set").all()
            .get(case_id=case_id)
        )

    def get_majority_class_from_tasks(self, case_id) -> Optional[str]:
        tasks = CaseManager.get_with_task_set_by_case_id(case_id).task_set.all()
        
        votes = {}
        for task in tasks:
            cat = task.category
            if cat is None:
                continue

            if cat in votes:
                votes[cat] += 1
            else:
                votes[cat] = 1

        max_vote = 0
        max_cat = None
        for cat, vote in votes.items():
            if vote > max_vote:
                max_vote = vote
                max_cat = cat
        
        return max_cat

    @staticmethod
    def bulk_update(cases: List[CaseModel], fields: List[str]):
        return CaseModel.objects.bulk_update(objs=cases, fields=fields)

    @staticmethod
    def filter_by_status(status: str, qs: Optional[QuerySet]=None):
        if qs is None:
            qs = CaseModel.objects.all()
        
        return qs.filter(status=status)

    @staticmethod
    def filter_by_products(products: Iterable, qs: Optional[QuerySet]=None):
        if qs is None:
            qs = CaseModel.objects.all()

        return qs.filter(product_name__in=products)

    @staticmethod
    def filter_by_batch_nos(batch_nos: Iterable, qs: Optional[QuerySet]=None):
        if qs is None:
            qs = CaseModel.objects.all()

        return qs.filter(batch_no__in=batch_nos)

    @staticmethod
    def filter_by_locations(locations: Iterable, qs: Optional[QuerySet]=None):
        if qs is None:
            qs = CaseModel.objects.all()

        return qs.filter(location__in=locations)

    @staticmethod
    def filter_by_issues(issues: Iterable, qs: Optional[QuerySet]=None):
        if qs is None:
            qs = CaseModel.objects.all()

        return qs.filter(product_issue__in=issues)

    @staticmethod
    def filter_by_date_range(
        start=None,
        end=None,
        qs: Optional[QuerySet]=None
    ):
        if qs is None:
            qs = CaseModel.objects.all()
        if start:
            start = DatetimeHelper.to_datetime(start)
            qs = qs.filter(created_at__gte=start)
        if end:
            end = DatetimeHelper.to_datetime(end)
            qs = qs.filter(created_at__lte=end)

        return qs


class TaskManager:
    @staticmethod
    def get_by_id(id: str):
        return TaskModel.objects.get(id=id)
    
    @staticmethod
    def get_by_case_id(case_id: str):
        return TaskModel.objects.filter(case__case_id=case_id)

    @staticmethod
    def bulk_update(tasks: Iterable[TaskModel], fields: List[str]):
        return TaskModel.objects.bulk_update(tasks, fields=fields)
