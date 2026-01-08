from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        
class ProductCreate(BaseModel):
    name: str
    category: str | None = None
    price: float


class ProductResponse(BaseModel):
    product_id: int
    name: str
    category: str | None
    price: float

    class Config:
        from_attributes = True
        
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    product_id: int
    quantity: int
    order_date: datetime

    class Config:
        from_attributes = True
