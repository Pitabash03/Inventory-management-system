from app.models import Product, Customer, Order
from app.schemas import *
from sqlalchemy.orm import Session

def create_product(db: Session, product: ProductCreate):
    try:
        item = Product(**product.dict())

        db.add(item)

        db.commit()

        db.refresh(item)

        return item

    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def create_customer(db: Session, customer: CustomerCreate):
    item = Customer(**customer.dict())
    db.add(item)
    db.commit()
    return item


def create_order(db: Session, order: OrderCreate):

    product = db.query(Product).filter(Product.id == order.product_id).first()

    if not product:
        return {"error": "Product not found"}

    if product.stock < order.quantity:
        return {"error": "Insufficient stock"}

    product.stock -= order.quantity

    new_order = Order(**order.dict())

    db.add(new_order)

    db.commit()

    return {"message": "Order created"}