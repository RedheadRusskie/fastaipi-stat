from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from uuid import UUID


class DatasetRowCreateDTO(BaseModel):
    dataset_id: UUID
    data: Dict[str, Any]


class DatasetRowUpdateDTO(BaseModel):
    data: Dict[str, Any]


class DatasetRowResponseDTO(DatasetRowCreateDTO):
    id: UUID
    created_at: datetime
