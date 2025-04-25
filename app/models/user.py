from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    hashed_password = Column(String, nullable=False)
    datasets = relationship("Dataset", backref="user", cascade="all, delete-orphan")
