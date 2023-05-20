import csv
from datetime import datetime
from typing import Dict

from django.core.management.base import BaseCommand

from src.cases.models import CaseModel
from src.cases.define import (
    CASE_STATUS_PENDING, 
    CASE_STATUS_RESOLVED,
    PRODUCT_ISSUE_PKG_INFO,
    PRODUCT_ISSUE_PKG_DAMAGED,
    PRODUCT_ISSUE_SENSUAL,
    PRODUCT_ISSUE_FOREIGN_MATTER,
    PRODUCT_ISSUE_AMOUNT,
)


class Command(BaseCommand):
    help = "Load data for `CaseModel` from the given csv"

    ISSUE_DICT = {
        "包裝上的資訊": PRODUCT_ISSUE_PKG_INFO,
        "包裝受損": PRODUCT_ISSUE_PKG_DAMAGED,
        "感官的": PRODUCT_ISSUE_SENSUAL,
        "異物": PRODUCT_ISSUE_FOREIGN_MATTER,
        "重量/體積/數量": PRODUCT_ISSUE_AMOUNT,
    }

    def add_arguments(self, parser):
        parser.add_argument("src", type=str, help="file path to be loaded")

    def handle(self, *args, **options):
        src = options["src"]

        with open(src, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            
            case_model_list = [
                CaseModel(
                    case_id=row["個案號碼"],
                    status=self._parse_status(row),
                    product_name=row["產品名稱"],
                    batch_no=row["產品批號"],
                    product_specs=row["產品規格"],
                    location=row["新加坡"],
                    product_issue=self._parse_product_issue(row),
                    issue_details=row["客訴詳細資訊"],
                    oem_feedback=row["原廠 feedback "],
                    oem_status=row["原廠 feedback \nStatus"],
                    created_at=self._parse_created_at(row),
                )
                for row in reader
            ]
            
            CaseModel.objects.bulk_create(case_model_list)

    def _parse_status(self, row: Dict[str, str]) -> str:
        status = row["狀態"]

        if "未結案" in status:
            return CASE_STATUS_PENDING
        elif "已結案" in status:
            return CASE_STATUS_RESOLVED
        else:
            raise AssertionError

    def _parse_product_issue(self, row: Dict[str, str]) -> str:
        issue_chi = row["產品問題"]
        issue_eng = self.ISSUE_DICT.get(issue_chi)

        if issue_eng is None:
            raise AssertionError

        return issue_eng

    def _parse_created_at(self, row: Dict[str, str]) -> datetime:
        
        d = datetime.strptime(row["立案日期"], "%Y/%m/%d")
        return d
