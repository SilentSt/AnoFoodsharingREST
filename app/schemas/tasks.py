from typing import List
from uuid import UUID

from pydantic import BaseModel


class AddressModel(BaseModel):
    id: int
    address: str
    shop: bool


class TasksModel(BaseModel):
    status: bool
    document_path: bool
    organization: AddressModel
    recipients: List[AddressModel]

