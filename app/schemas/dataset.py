from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.schemas.dataset_row import DatasetRowDTO


class DatasetDTO(BaseModel):
    name: str
    description: str


class DatasetResponseDTO(DatasetDTO):
    id: UUID
    rows: List[DatasetRowDTO] = []
