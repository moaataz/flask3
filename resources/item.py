from flask.app import Flask
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    with Flask(__name__).test_request_context():
        parser = reqparse.RequestParser()
        parser.add_argument('price',type=float,help="you should type price")
        parser.add_argument('store_id',type=float,help="you should type store_id")
        data = parser.parse_args()
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'},404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':f'item with name {name} already exists'},400
        data = Item.parser.parse_args()
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {'message':'an error occured'},500
        return item, 201
    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item deleted'}
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            try:
                item = ItemModel(name,**data)
            except:
                return {'message':'an error occured'},500
        else:
            try:
                item.price = data['price']
            except:
                return {'message':'an error occured'},500
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        items = []
        for row in ItemModel.query.all():
            items.append(row)
        return {'items':items}