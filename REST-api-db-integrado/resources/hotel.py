from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hotels = [
  {
    'hotel_id': '1',
    'nome': 'Alpha hotel',
    'estrelas': 4.9,
    'diaria': 450.36,
    'cidade': 'Jeri'
  },
  {
    'hotel_id': '2',
    'nome': 'Beta hotel',
    'estrelas': 4.2,
    'diaria': 500.36,
    'cidade': 'Guaramiranga'
  },
  {
    'hotel_id': '3',
    'nome': 'Bruna hotel',
    'estrelas': 2.1,
    'diaria': 150.66,
    'cidade': 'Fortaleza'
  }
]

class Hotels(Resource):
  def get(self):
    # hotels = HotelModel.json()
    return {'hotels': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
  args1 = reqparse.RequestParser()
  args1.add_argument('name', type=str, required=True, help="the filed 'name' cant be left blank")
  args1.add_argument('stars', type=float, required=True, help="the field stars cant be lef blank")
  args1.add_argument('price')
  args1.add_argument('city')

  # def find_hotel(hotel_id):
  #   for hotel in hoteis:
  #     if hotel_id == hotel['hotel_id']:
  #       return hotel
  #   return None

  def get(self,hotel_id):
    hotel = HotelModel.find_hotel(hotel_id)
    if hotel:
      return hotel.json(), 200
    return {'message':'Hotel Not Found.'}, 404

  def post(self,hotel_id):
    if HotelModel.find_hotel(hotel_id):
      return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 # bad request
    
    data = Hotel.args1.parse_args()
    hotel = HotelModel(hotel_id, **data)
    
    try:
      hotel.save_hotel() ## save on db
      return hotel.json(), 200
    except:
      return {'message': 'An internal error occurrend trying to save hotel'}, 500
    
    
    # new_hotel=hotel.json()

    # hoteis.append(new_hotel)
    

  def put(self,hotel_id):
    data = Hotel.args1.parse_args()  

    finded_hotel = HotelModel.find_hotel(hotel_id)
    if finded_hotel:
      finded_hotel.update_hotel(**data)
      try:
        hotel.save_hotel() ## save on db
        return finded_hotel.json(), 200
      except:
        return {'message': 'An internal error occurrend trying to save hotel'}, 500  

    hotel = HotelModel(hotel_id, **data)

    try:
      hotel.save_hotel() ## save on db
    except:
      return {'message': 'An internal error occurrend trying to save hotel'}, 500
    
    
    return hotel.json(), 201

  def delete(self,hotel_id):
    hotel = HotelModel.find_hotel(hotel_id)
    if hotel:
      try:
        hotel.delete_hotel()
        return {'message': 'Hotel deleted.'}
      except:
        return {'message': 'An internal error occurrend trying to delete hotel'}, 500

    return {'message': 'HOtel not found'}, 404

### alguns comandos
'''
 ### POST: 
 curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"name":"xyz","stars":2.6,"price":180.50,"city":"Fortaleza"}' \
    http://localhost:5000/hotels/4

  ### PUT:
   curl --header "Content-Type: application/json" \
    --request PUT \
    --data '{"name":"xyz","stars":2.6,"price":180.50,"city":"Fortaleza"}' \
    http://localhost:5000/hotels/4

  ### DELETE:
  curl -X DELETE http://localhost:5000/hotels/3

'''