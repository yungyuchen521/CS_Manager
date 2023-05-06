from typing import Iterable, Optional

from django.db.models import QuerySet

from src.cases.models import CaseModel
from src.utils import DatetimeHelper


class CaseManager:
    @staticmethod
    def get_by_case_id(case_id: str):
        return CaseModel.objects.get(case_id=case_id)

    @staticmethod
    def get_case_and_task_set_by_id(case_id: str):
        return (
            CaseModel.objects
            .select_related("task_set")
            .get(case_id=case_id)
        )

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
