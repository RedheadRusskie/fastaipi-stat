from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base
import uuid

class DatasetRow(Base):
    __tablename__ = "dataset_row"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("dataset.id", ondelete="CASCADE"), nullable=False)
    data = Column(JSONB, nullable=False)
