from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    stock: int


class CustomerCreate(BaseModel):
    name: str
    email: str


class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int



class CustomerCreate(BaseModel):
    name: str
    email: str


class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int