from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Any


class DatasetRowDTO(BaseModel):
    dataset_id: UUID
    data: Dict[str, Any]
