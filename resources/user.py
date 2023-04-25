from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt
from blacklist import BLACKLIST

parser = reqparse.RequestParser()
parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
class UserRegister(Resource):

    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    def get(self,user_id:int):
        user = UserModel.find_by_id(user_id).first()
        if not user:
            return {'message':'user not found'},404
        return user.json()

    def delete(self,user_id:int):
        user = UserModel.find_by_id(user_id).first()
        if not user:
            return {'message':'user not found'},404
        user.delete_from_db()
        return {'message':'user deleted'},200

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and compare_digest(user.password,data['password']):
            access_token = create_access_token(user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token,
            },201
        
        return {'message':'invalid credientals'},401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] # jti is "jwt id", a unique identifier for a jwt
        BLACKLIST.add(jti)
        return {'message':'successfully logged out'},201

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt()
        new_token = create_access_token(identity=current_user['identity'],fresh=False)
        return {'access_token':new_token},200