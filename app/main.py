from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.models import  payment  # 导入所有模型
from app.routers.payment_service import payment_router  # 导入支付相关的 router
from fastapi.middleware.cors import CORSMiddleware
from app.config.log import setup_logger
from app.config.cloudwatch_logger import setup_cloudwatch_logger
from app.dependencies.logging_middleware import logging_dependency
service_name = "payment-service"
logger = setup_cloudwatch_logger(service_name)

payment.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = setup_logger()
app.middleware("http")(logging_dependency)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
app.middleware("http")(logging_dependency)

app.include_router(payment_router, prefix="/payments", tags=["payments"])


@app.get("/")
def read_root():
    return {"Hello": "World"}