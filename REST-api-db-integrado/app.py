from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db' ## it create a db of type sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'CHAVEGARANTECRIPTOGRAFIA'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_db():
  database1.create_all()

@jwt.token_in_blacklist_loader
def verify_blacklist(token):
  return token['jti'] in BLACKLIST

## acesso revogado
@jwt.revoked_token_loader
def token_access_invalid():
  return jsonify({'message':'You have been logged out'}), 401 # unauthorized

## criando recurso que se extende por hoteis 
## http://127.0.0.1:5000/hoteis
api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:hotel_id>')
api.add_resource(User,'/users/<int:user_id>')
api.add_resource(UserRegister, '/signup')
api.add_resource(UserLogin,'/login')
api.add_resource(UserLogout,'/logout')

if __name__ == '__main__':
  from sql_alchemy import database1
  database1.init_app(app)

  app.run(debug=True)