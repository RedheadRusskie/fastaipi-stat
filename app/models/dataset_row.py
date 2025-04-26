from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone
import uuid
from app.db.base import Base


class DatasetRow(Base):
    __tablename__ = "dataset_row"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id = Column(
        UUID(as_uuid=True), ForeignKey("dataset.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    data = Column(JSONB, nullable=False)
