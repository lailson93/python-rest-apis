from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db' ## it create a db of type sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

@app.before_first_request
def create_db():
  database1.create_all()

## criando recurso que se extende por hoteis 
## http://127.0.0.1:5000/hoteis
api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:hotel_id>')

if __name__ == '__main__':
  from sql_alchemy import database1
  database1.init_app(app)

  app.run(debug=True)