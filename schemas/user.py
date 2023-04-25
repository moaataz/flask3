from models.user import UserModel
from ma import marsh


class UserSchema(marsh.SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
