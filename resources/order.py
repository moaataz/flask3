from flask_restful import Resource, request
from models.item import ItemModel

from models.order import OrderModel


class Order(Resource):
    def post(self):
        data = request.get_json()
        items = []

        for _id in data["item_ids"]:
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message": "item not found"}, 404
            items.append(item)
        order = OrderModel(orders=items, status="pending")
        order.save_to_db()
