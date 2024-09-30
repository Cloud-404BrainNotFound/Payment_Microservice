from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.models import  payment  # 导入所有模型

from app.routers.payment_service.payment_service import payment_router  # 导入支付相关的 router


# 创建数据库表

payment.Base.metadata.create_all(bind=engine)


app = FastAPI()


# 这是一个router的示例

app.include_router(payment_router, prefix="/payments", tags=["payments"])


@app.get("/")
def read_root():
    return {"Hello": "World"}