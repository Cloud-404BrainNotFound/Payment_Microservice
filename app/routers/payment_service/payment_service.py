from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.database import get_db
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from typing import List
from enum import Enum


# class PaymentStatus(Enum):
#     PENDING = "PENDING"
#     COMPLETED = "COMPLETED"
#     FAILED = "FAILED"

# class PaymentMethodType(Enum):
#     CREDIT_CARD = "CREDIT_CARD"
#     DEBIT_CARD = "DEBIT_CARD"

class PaymentStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class PaymentMethodType(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PAYPAL = "PAYPAL"

payment_router = APIRouter()

class UserPaymentRequest(BaseModel):
    user_id: str
class UpdatePaymentStatusRequest(BaseModel):
    payment_id: int
    status: str

class Status(BaseModel):
    status: str
class PaymentCreate(BaseModel):
    user_id: str
    order_id: str
    amount: float
    currency: str = "USD"
    status: str
    method: str
    transaction_id: Optional[str] = ""

class PaymentResponse(BaseModel):
    message: str
    payment_id: str


@payment_router.get("/payment_check/{payment_id}")
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"payment_id": payment.id, "user_id": payment.user_id, "amount": payment.amount,"currency": payment.currency}


# @payment_router.get("/user_check/{user_id}")
# def get_payments_by_user(user_id: str, db: Session = Depends(get_db)) -> List[dict]:
#     # 查询数据库以获取所有属于特定用户的支付记录
#     payments = db.query(Payment).filter(Payment.user_id == user_id).all()
#     if not payments:
#         raise HTTPException(status_code=404, detail="No payments found for the user")
#     # 返回一个包含所有支付记录的列表
#     return [
#         {
#             "payment_id": payment.id,
#             "user_id": payment.user_id,
#             "order_id": payment.order_id,
#             "amount": payment.amount,
#             "currency": payment.currency,
#             "status": payment.status,
#             "method": payment.method,
#             "transaction_id": payment.transaction_id,
#             "created_at": payment.created_at,
#             "updated_at": payment.updated_at
#         }
#         for payment in payments
#     ]

@payment_router.post("/search")  # 修改路由路径和方法
def get_payments_by_user(request: UserPaymentRequest, db: Session = Depends(get_db)) -> List[dict]:
    user_id = request.user_id
    payments = db.query(Payment).filter(Payment.user_id == user_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for the user")
    return [
        {
            "payment_id": payment.id,
            "user_id": payment.user_id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
            "method": payment.method,
            "transaction_id": payment.transaction_id,
            "created_at": payment.created_at,
            "updated_at": payment.updated_at
        }
        for payment in payments
    ]


@payment_router.post("/add_payment")
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(
        user_id=payment_data.user_id,
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        currency=payment_data.currency,
        status=payment_data.status,
        method=payment_data.method,
        transaction_id=payment_data.transaction_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_payment)
    db.commit()
    return PaymentResponse(message="Payment created successfully", payment_id=new_payment.id)

@payment_router.post("/update_status")
def update_payment_status(payment_data: UpdatePaymentStatusRequest, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_data.payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = payment_data.status
    db.commit()
    return Status(status="Payment status updated successfully")
