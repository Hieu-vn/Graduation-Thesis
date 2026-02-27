"""
Read-only database models mirroring SmartFinanceBE tables.
AI service only reads these tables, never writes to them.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, Date
from sqlalchemy.orm import relationship

from app.core.database import Base


# ============================================================
# Models mirrored from SmartFinanceBE (read-only)
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)

    accounts = relationship("Account", back_populates="user", viewonly=True)
    budgets = relationship("Budget", back_populates="user", viewonly=True)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String(10), default="VND")
    institution = Column(String(255), nullable=True)
    created_at = Column(DateTime)

    user = relationship("User", back_populates="accounts", viewonly=True)
    transactions = relationship("Transaction", back_populates="account", viewonly=True)


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False)
    is_default = Column(Boolean, default=False)

    transactions = relationship("Transaction", back_populates="category", viewonly=True)
    budgets = relationship("Budget", back_populates="category", viewonly=True)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True)
    account_id = Column(String(36), ForeignKey("accounts.id"), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="VND")
    description = Column(String(500), nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime)

    account = relationship("Account", back_populates="transactions", viewonly=True)
    category = relationship("Category", back_populates="transactions", viewonly=True)


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="VND")
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    user = relationship("User", back_populates="budgets", viewonly=True)
    category = relationship("Category", back_populates="budgets", viewonly=True)


# ============================================================
# AI-owned model (read-write)
# ============================================================

class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    session_id = Column(String(36), nullable=False, index=True)
    role = Column(
        Enum("user", "assistant", name="chat_role"),
        nullable=False,
    )
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", viewonly=True)
