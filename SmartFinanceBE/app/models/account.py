import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core.database import Base

AccountType = Enum(
    "checking", "savings", "credit_card", "investment", "loan", "cash", "crypto", "other",
    name="account_type"
)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(AccountType, nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String(10), default="VND")
    institution = Column(String(255), nullable=True)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    holdings = relationship("Holding", back_populates="account", cascade="all, delete-orphan")
