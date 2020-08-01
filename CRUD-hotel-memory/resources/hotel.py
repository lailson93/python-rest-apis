from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
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

## a biblioteca do flask_restful converte automaticmente dic em json
## adicionando recurso (class, path)
## criando recurso hoteis (collection)
class Hoteis(Resource):
  # localhost/hoteis
  def get(self):
    return {'hoteis': hoteis} 

### criando recurso hotel (instancia)
class Hotel(Resource):
  argumentos = reqparse.RequestParser()
  argumentos.add_argument('nome')
  argumentos.add_argument('estrelas')
  argumentos.add_argument('diaria')
  argumentos.add_argument('cidade')

  def find_hotel(hotel_id):
    for hotel in hoteis:
      if hotel['hotel_id'] == hotel_id:
        return hotel
    return None

  # localhost/hoteis/{hotel_id}
  def get(self,hotel_id):
    hotel = Hotel.find_hotel(hotel_id)
    if hotel:
      return hotel
    return {'message':'Hotel not found.'}, 404 # not found

    # curl localhost:5000/hoteis/3

  def post(self,hotel_id):
    ## como requirement é preciso do reqparse
    
    dados = Hotel.argumentos.parse_args()
    hotel_objeto = HotelModel(hotel_id, **dados)

    novo_hotel=hotel_objeto.json()

    hoteis.append(novo_hotel)
    return novo_hotel, 200

    #   curl --header "Content-Type: application/json" \
    # --request POST \
    # --data '{"nome":"xyz","estrelas":2.6,"diaria":180.50,"cidade":"Fortaleza"}' \
    # http://localhost:5000/hoteis/4

  ## O PUT faz alteracoes nos dados
  def put(self,hotel_id): 

    dados = Hotel.argumentos.parse_args()  
    hotel_objeto = HotelModel(hotel_id, **dados)
    novo_hotel = hotel_objeto.json()

    hotel = Hotel.find_hotel(hotel_id)
    if hotel:
      hotel.update(novo_hotel)
      return novo_hotel, 200
    hoteis.append(novo_hotel)
    
    return novo_hotel, 201

    # curl --header "Content-Type: application/json" \
    #   --request PUT \
    #   --data '{"nome":"HOTEL FERREIRaaaa","estrelas":5,"diaria":180.50,"cidade":"Fortaleza"}' \
    #   http://localhost:5000/hoteis/5

  def delete(self,hotel_id):
    global hoteis
    hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
    return {'message': 'Hotel deleted.'}

    # curl -X DELETE http://localhost:5000/hoteis/3