from typing import Any, Dict, Optional

from fastapi import HTTPException


class MissingEmployeeRecord(HTTPException):
    def __init__(
        self,
        status_code,
        detail: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
