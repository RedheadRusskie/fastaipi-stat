from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base
import uuid
from sqlalchemy.orm import relationship

class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    rows = relationship("DatasetRow", backref="dataset", cascade="all, delete-orphan")
