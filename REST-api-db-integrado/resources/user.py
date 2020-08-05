from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


args1 = reqparse.RequestParser()
args1.add_argument('login', type=str, required=True, help="The field login cannot be left blank")
args1.add_argument('password', type=str, required=True, help="The field password cannot be left blank")


class User(Resource):

  ## /users/{user_id}
  def get(self,user_id):
    user = UserModel.find_user(user_id)
    if user:
      return user.json(), 200
    return {'message':'User Not Found.'}, 404

  @jwt_required
  def delete(self,user_id):
    user = UserModel.find_user(user_id)
    if user:
      try:
        user.delete_user()
        return {'message': 'User deleted.'}
      except:
        return {'message': 'An internal error occurrend trying to delete user'}, 500

    return {'message': 'User not found'}, 404

class UserRegister(Resource):
  # /signup
  def post(self):

    data = args1.parse_args()

    if UserModel.find_by_login(data['login']):
      return {"message":"The login '{}' already exists".format(data['login'])}

    user = UserModel(**data)
    user.save_user()
    return {'message':'User created successfully'}, 201

class UserLogin(Resource):
  ## pip install Flask-JWT-Extended

  @classmethod
  def post(cls):
    data = args1.parse_args()
    user = UserModel.find_by_login(data['login'])

    if user and safe_str_cmp(user.password, data['password']):
      token_access = create_access_token(identity=user.user_id)
      return {'access_token': token_access}, 200
    return {'message':'the username or password is incorrect'}, 401

class UserLogout(Resource):
  @jwt_required
  def post(self):
    jwt_id = get_raw_jwt()['jti'] #jwt token identifier
    BLACKLIST.add(jwt_id)
    return {'message':'Logged out successfully'}, 200




### alguns comandos
'''
 ### POST: 
 curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"login":"admin2","password":"123456"}' \
    http://localhost:5000/signup


  ### DELETE:
  curl -X DELETE http://localhost:5000/users/3


 curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"login":"admin2","password":"123456"}' \
    http://localhost:5000/login

'''