from app.models import Product, Customer, Order
from app.schemas import ProductCreate, CustomerCreate, OrderCreate
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import crud, schemas
from app.models import Product, Customer, Order


Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Inventory Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Inventory API Running"}


@app.post("/products")
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@app.post("/customers")
def add_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@app.post("/orders")
def add_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    orders = db.query(Order).filter(Order.product_id == product_id).first()

    if orders:
        return {"error": "Cannot delete product. Orders exist."}

    db.delete(product)

    db.commit()

    return {"message": "Product deleted"}

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: schemas.ProductCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    product.name = updated_product.name
    product.price = updated_product.price
    product.stock = updated_product.stock
    product.sku = updated_product.sku

    db.commit()

    db.refresh(product)

    return {
        "message": "Product updated",
        "product": product
    }


@app.post("/customers")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):

    new_customer = Customer(
        name=customer.name,
        email=customer.email
    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    return new_customer


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):

    return db.query(Customer).all()




@app.post("/orders")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == order.product_id).first()

    if not product:
        return {"error": "Product not found"}

    if product.stock < order.quantity:
        return {"error": "Insufficient stock"}

    product.stock -= order.quantity

    new_order = Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity
    )

    db.add(new_order)

    db.commit()

    return {"message": "Order created"}

