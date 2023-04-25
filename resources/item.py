from flask_restful import Resource, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from models.item import ItemModel
from schemas.item import ItemSchema

ITEM_NOT_FOUND = "Item not found"
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred inserting the item."
ITEM_DELETED = "Item deleted."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item)
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400
        data_json = request.get_json()
        data_json["name"] = name
        try:
            data = item_schema.load(data_json)
        except ValidationError as err:
            return err.messages, 400
        data.name = name

        try:
            data.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item_schema.dump(data), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name):
        item_json = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name
            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200
