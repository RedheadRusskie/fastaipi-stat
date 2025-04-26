from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.schemas.dataset_row import DatasetRowResponseDTO


class DatasetDTO(BaseModel):
    name: str
    description: Optional[str] = None


class DatasetResponseDTO(DatasetDTO):
    id: UUID
    created_at: datetime
    rows: List[DatasetRowResponseDTO] = []
