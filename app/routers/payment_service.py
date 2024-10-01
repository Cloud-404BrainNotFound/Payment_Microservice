from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus
from app.database import get_db
from pydantic import BaseModel, Field

payment_router = APIRouter()

class PaymentCreate(BaseModel):
    card_number: str = Field(..., min_length=16, max_length=16)  # Must be exactly 16 digits
    expiry_month: str = Field(..., min_length=2, max_length=2)  # MM format
    expiry_year: str = Field(..., min_length=2, max_length=2)   # YY format
    cvc: str = Field(..., min_length=3, max_length=3)  # CVC must be 3 digits

class PaymentResponse(BaseModel):
    message: str
    payment_id: str

@payment_router.post("/add_payment", response_model=PaymentResponse)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    try:
        new_payment = Payment(
            card_number=payment_data.card_number,
            expiry_month=payment_data.expiry_month,
            expiry_year=payment_data.expiry_year,
            cvc=payment_data.cvc,
            status=PaymentStatus.COMPLETED  
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return PaymentResponse(message="Payment created successfully", payment_id=new_payment.id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
