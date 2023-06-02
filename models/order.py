import os

from db import db
from typing import List

item_to_orders = db.Table(
    "items_to_orders",
    db.Column(
        "item_id",
        db.Integer,
        db.ForeignKey("items.id"),
    ),
    db.Column(
        "order_id",
        db.Integer,
        db.ForeignKey("orders.id"),
    ),
)


class ItemInOrder(db.Model):
    __tablename__ = "item_in_orders"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel", back_populates="items")


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    items = db.relationship("ItemInOrder", back_populates="order", lazy="dynamic")

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id) -> "OrderModel":
        return cls.query.filter_by(id=id).first()

    def set_status(self, new_status) -> None:
        self.status = new_status
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
