from models.user import UserModel
from ma import marsh


class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True

        load_only = ("password",)
        dump_only = ("id",)
