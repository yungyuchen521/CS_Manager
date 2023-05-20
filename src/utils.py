from typing import Dict, Optional, Union
from datetime import datetime, date

from rest_framework import status
from rest_framework.response import Response


class ResponseHelper:
    @classmethod
    def item_not_found_resp(cls, item: str) -> Response:
        MSG = f"no such {item}"

        return Response(
            data=cls._build_error_data(msg=MSG),
            status=status.HTTP_404_NOT_FOUND,
        )

    @classmethod
    def error_resp(cls, msg: str, status_code, **kwargs) -> Response:
        data = cls._build_error_data(msg, **kwargs)

        return Response(
            data=data,
            status=status_code,
        )

    @classmethod
    def verify_content_type(cls, expected_type: str, actual_type: str) -> Optional[Response]:
        if expected_type == actual_type:
            return

        MSG = "expected {expected_type} but {actual_type} received"
        data = cls._build_error_data(
            msg=MSG,
            expected_type=expected_type,
            actual_type=actual_type,
        )

        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _build_error_data(msg: str, **kwargs) -> Dict[str, str]:
        if kwargs:
            msg = msg.format(**kwargs)
        
        return {"error": msg.format(**kwargs)}


class DatetimeHelper:
    D_FMT = ["%Y-%m-%d"]
    DT_FMT = []

    @classmethod
    def to_datetime(cls, string) -> Union[datetime, date]:
        if isinstance(string, (datetime, date)):
            return string
        elif not isinstance(string, str):
            raise ValueError(f"expected `datetime`, `date` or `str` but {type(string)} received")

        try:
            return datetime.fromisoformat(string)
        except ValueError:
            pass

        for fmt in cls.D_FMT + cls.DT_FMT:
            try:
                return datetime.strptime(string, fmt)
            except ValueError:
                pass
        
        raise ValueError(f"unexpected date time format `{string}`")
