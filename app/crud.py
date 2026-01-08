from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy import func

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        category=product.category,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
    

def create_order(db: Session, order: schemas.OrderCreate):

    user = db.query(models.User).filter(models.User.user_id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = db.query(models.Product).filter(models.Product.product_id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_order = models.Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_total_revenue(db: Session):
    result = (
        db.query(func.sum(models.Product.price * models.Order.quantity))
        .join(models.Order, models.Product.product_id == models.Order.product_id)
        .scalar()
    )
    return result or 0


def get_revenue_per_user(db: Session):
    results = (
        db.query(
            models.User.user_id,
            models.User.name,
            func.sum(models.Product.price * models.Order.quantity).label("total_revenue")
        )
        .join(models.Order, models.User.user_id == models.Order.user_id)
        .join(models.Product, models.Product.product_id == models.Order.product_id)
        .group_by(models.User.user_id)
        .all()
    )
    return results


def get_top_products(db: Session, limit: int = 5):
    results = (
        db.query(
            models.Product.product_id,
            models.Product.name,
            func.sum(models.Order.quantity).label("total_quantity")
        )
        .join(models.Order, models.Product.product_id == models.Order.product_id)
        .group_by(models.Product.product_id)
        .order_by(func.sum(models.Order.quantity).desc())
        .limit(limit)
        .all()
    )
    return results

