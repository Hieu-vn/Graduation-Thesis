import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = Column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    type = Column(
        Enum("income", "expense", "transfer", name="transaction_type"),
        nullable=False,
    )
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="VND")
    description = Column(String(500), nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
