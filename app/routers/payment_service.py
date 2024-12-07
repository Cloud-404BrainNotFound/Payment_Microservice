from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.payment import Payment, PaymentStatus
from app.database import get_db

payment_router = APIRouter()

# 创建支付请求模型
class PaymentCreate(BaseModel):
    card_number: str = Field(..., min_length=16, max_length=16)  # 卡号必须为16位
    expiry_month: str = Field(..., min_length=2, max_length=2)  # 月份 MM 格式
    expiry_year: str = Field(..., min_length=2, max_length=2)   # 年份 YY 格式
    cvc: str = Field(..., min_length=3, max_length=3)  # CVC 必须为3位数字

# 更新支付记录模型
class PaymentUpdate(BaseModel):
    expiry_month: Optional[str] = Field(None, min_length=2, max_length=2)
    expiry_year: Optional[str] = Field(None, min_length=2, max_length=2)
    cvc: Optional[str] = Field(None, min_length=3, max_length=3)
    status: Optional[PaymentStatus]

# 支付记录返回模型
class PaymentDetail(BaseModel):
    id: str
    card_number: str
    expiry_month: str
    expiry_year: str
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

# 创建支付记录返回模型
class PaymentResponse(BaseModel):
    message: str
    payment_id: str

# 创建支付记录
@payment_router.post("/payments", response_model=PaymentResponse)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    try:
        new_payment = Payment(
            card_number=payment_data.card_number,
            expiry_month=payment_data.expiry_month,
            expiry_year=payment_data.expiry_year,
            cvc=payment_data.cvc,
            status=PaymentStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return PaymentResponse(message="Payment created successfully", payment_id=new_payment.id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

# 获取单个支付记录
@payment_router.get("/payments/{payment_id}", response_model=PaymentDetail)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentDetail(
        id=payment.id,
        card_number=payment.card_number,
        expiry_month=payment.expiry_month,
        expiry_year=payment.expiry_year,
        status=payment.status,
        created_at=payment.created_at,
        updated_at=payment.updated_at
    )

# 更新支付记录
@payment_router.put("/payments/{payment_id}", response_model=PaymentDetail)
def update_payment(payment_id: str, payment_data: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment_data.expiry_month:
        payment.expiry_month = payment_data.expiry_month
    if payment_data.expiry_year:
        payment.expiry_year = payment_data.expiry_year
    if payment_data.cvc:
        payment.cvc = payment_data.cvc
    if payment_data.status:
        payment.status = payment_data.status
    payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return PaymentDetail(
        id=payment.id,
        card_number=payment.card_number,
        expiry_month=payment.expiry_month,
        expiry_year=payment.expiry_year,
        status=payment.status,
        created_at=payment.created_at,
        updated_at=payment.updated_at
    )

# 删除支付记录
@payment_router.delete("/payments/{payment_id}", response_model=PaymentResponse)
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return PaymentResponse(message="Payment deleted successfully", payment_id=payment_id)

# 获取所有支付记录
@payment_router.get("/payments", response_model=List[PaymentDetail])
def get_all_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    return [
        PaymentDetail(
            id=payment.id,
            card_number=payment.card_number,
            expiry_month=payment.expiry_month,
            expiry_year=payment.expiry_year,
            status=payment.status,
            created_at=payment.created_at,
            updated_at=payment.updated_at
        ) for payment in payments
    ]