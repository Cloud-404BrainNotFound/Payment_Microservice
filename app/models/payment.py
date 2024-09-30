from sqlalchemy import Column, String, Float, Enum as SQLEnum, DateTime, JSON, Boolean
from app.database import Base
from datetime import datetime
import uuid
import enum

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class PaymentMethodType(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    order_id = Column(String(36), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    method = Column(SQLEnum(PaymentMethodType), default=PaymentMethodType.CREDIT_CARD)
    transaction_id = Column(String(255), default="")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    extra = Column(JSON, default={})

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    type = Column(SQLEnum(PaymentMethodType), default=PaymentMethodType.CREDIT_CARD)
    details = Column(JSON, default={})
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)