from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout

from ma import marsh
from db import db

from resources.item import Item, ItemList
from marshmallow import ValidationError
from resources.store import Store, StoreList
from resources.image import UploadImage, Image, AvatarUpload
from blacklist import BLACKLIST
from dotenv import load_dotenv
from flask_uploads import configure_uploads, patch_request_class
from libs.image_helper import IMAGE_SET

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
api = Api(app)


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


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


def create_db():
    with app.app_context():
        db.create_all()


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UploadImage, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")

if __name__ == "__main__":
    marsh.init_app(app)
    db.init_app(app)
    create_db()
    app.run(port=5000)
