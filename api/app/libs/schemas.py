
from typing import List, Optional, Dict, Any

from pydantic import BaseModel


class QueryArgsPagination(BaseModel):
    limit: Optional[int] = 10
    page: Optional[int] = 1


class ResponseMessageOut(BaseModel):
    message: str = 'Ok'


class ResponseDataListOut(BaseModel):
    data: List[Dict[str, Any]]


class ResponseDataItemOut(BaseModel):
    data: Dict[str, Any]


class ResponseMessageDataItemOut(ResponseMessageOut, ResponseDataItemOut):
    pass


class ResponseMessageDataListOut(ResponseMessageOut, ResponseDataListOut):
    pass
