from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout

from ma import marsh
from db import db

from resources.item import Item, ItemList

from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "jose"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)  # /auth


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True, "identity": identity}
    else:
        return {"is_admin": False, "identity": identity}


@jwt.expired_token_loader
def expired_token_callback():
    return {
        "description": "the token has expired",
        "error": "token_expired",
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        "description": "signature verification failed",
        "error": "invalid_token",
    }, 401


@jwt.unauthorized_loader
def unauthorized_callback():
    return {
        "description": "user doesn't have access token",
        "error": "authorization_required",
    }, 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return {
        "description": "the token is not refresh",
        "error": "fresh_token_required",
    }, 401


@jwt.revoked_token_loader
def revoked_token_callback(_, __):
    return {"description": "the token has been revoked", "error": "token_revoked"}, 401


@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(_, decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    marsh.init_app(app)
    db.init_app(app)
    app.run(port=5000, debug=True)
