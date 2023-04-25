from ma import marsh
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema


class StoreSchema(marsh.SQLAlchemyAutoSchema):
    items = marsh.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        load_instance = True
        include_fk = True
        dump_only = ("id",)
