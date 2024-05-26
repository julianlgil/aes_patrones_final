from typing import Optional, Dict

from pydantic import BaseModel, ValidationError


class RequestInfo(BaseModel):
    path_operation: str
    method: Optional[str] = None
    payload: Optional[Dict] = None
    headers: Optional[Dict] = None
    path_params: Optional[Dict] = None
    query_params: Optional[Dict] = None
