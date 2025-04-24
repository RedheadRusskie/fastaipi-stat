from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.db.base import Base
from sqlalchemy.orm import relationship
import uuid


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    rows = relationship("DatasetRow", backref="dataset", cascade="all, delete-orphan")
