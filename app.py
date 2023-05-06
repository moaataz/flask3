from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv
from resources.user import UserRegister, UserLogin, User, SetPassword
from flask_migrate import Migrate

load_dotenv(".env")
from resources.github_login import GithubLogin, GithubAuthorize

from db import db
from ma import ma
from oa import oauth

app = Flask(__name__)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)


def create_tables():
    with app.app_context():
        db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(GithubLogin, "/login/github")
api.add_resource(GithubAuthorize, "/login/github/authorized")
api.add_resource(SetPassword, "/user/password")

if __name__ == "__main__":
    ma.init_app(app)
    create_tables()
    oauth.init_app(app)
    app.run(port=5000)
