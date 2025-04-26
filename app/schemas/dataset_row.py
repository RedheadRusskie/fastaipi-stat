from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Any, Optional


class DatasetRowDTO(BaseModel):
    id: Optional[UUID]
    dataset_id: UUID
    data: Dict[str, Any]
