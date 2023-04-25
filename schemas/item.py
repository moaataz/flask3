from models.item import ItemModel
from ma import marsh


class ItemSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        include_fk = True

        load_only = ("store",)
        dump_only = ("id",)
