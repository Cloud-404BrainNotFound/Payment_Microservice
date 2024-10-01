from sqlalchemy import Column, String, Enum as SQLEnum, DateTime
from app.database import Base
from datetime import datetime
import uuid
import enum

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    card_number = Column(String(16), nullable=False)  # Store as a string for fixed length
    expiry_month = Column(String(2), nullable=False)  # MM format
    expiry_year = Column(String(2), nullable=False)   # YY format
    cvc = Column(String(3), nullable=False)  # CVC
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
