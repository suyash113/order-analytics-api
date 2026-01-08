from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Analytics API")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@app.get("/analytics/revenue")
def total_revenue(db: Session = Depends(get_db)):
    return {
        "total_revenue": crud.get_total_revenue(db)
    }

@app.get("/analytics/revenue-per-user")
def revenue_per_user(db: Session = Depends(get_db)):
        data = crud.get_revenue_per_user(db)
        return [
            {
                "user_id": row.user_id,
                "name": row.name,
                "total_revenue": row.total_revenue
            } 
            for row in data
        ]

@app.get("/analytics/top-products")
def top_products(limit: int = 5, db: Session = Depends(get_db)):
    data = crud.get_top_products(db, limit)
    return [
        {
            "product_id": row.product_id,
            "name": row.name,
            "total_quantity": row.total_quantity
            }
        for row in data
    ]
