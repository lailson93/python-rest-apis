from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

# hotels = [
#   {
#     'hotel_id': '1',
#     'nome': 'Alpha hotel',
#     'estrelas': 4.9,
#     'diaria': 450.36,
#     'cidade': 'Jeri'
#   },
#   {
#     'hotel_id': '2',
#     'nome': 'Beta hotel',
#     'estrelas': 4.2,
#     'diaria': 500.36,
#     'cidade': 'Guaramiranga'
#   },
#   {
#     'hotel_id': '3',
#     'nome': 'Bruna hotel',
#     'estrelas': 2.1,
#     'diaria': 150.66,
#     'cidade': 'Fortaleza'
#   }
# ]


def normalize_path_params(city=None,
                          stars_min=0,
                          stars_max=5,
                          price_min=0,
                          price_max=10000,
                          limit=50,
                          offset=0,
                          **data):
    if city:
        return {
            'stars_min': stars_min,
            'stars_max': stars_max,
            'price_min': price_min,
            'price_max': price_max,
            'city': city,
            'limit': limit,
            'offset': offset
        }
    return {
        'stars_min': stars_min,
        'stars_max': stars_max,
        'price_min': price_min,
        'price_max': price_max,
        'limit': limit,
        'offset': offset
    }


# path /hotels?city=Fortaleza&stars_min=4&price_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('stars_min', type=float)
path_params.add_argument('stars_max', type=float)
path_params.add_argument('price_min', type=float)
path_params.add_argument('price_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset',
                         type=float)  #quant elementos q desejamos pular


class Hotels(Resource):
    def get(self):
        connection = sqlite3.connect('database1.db')
        cursor = connection.cursor()

        # hotels = HotelModel.json()
        data = path_params.parse_args()
        #{'limit':50,'price_min': None}
        data_validos = {
            chave: data[chave]
            for chave in data if data[chave] is not None
        }

        params = normalize_path_params(**data_validos)

        if not params.get('city'):
            query1 = "SELECT * FROM hotels \
            WHERE (stars > ?) AND (stars < ?)\
              AND (price > ?) AND (price < ?)\
              LIMIT ? OFFSET ?"

            tupla1 = tuple([params[chave] for chave in params])
            result = cursor.execute(query1, tupla1)
        else:
            query1 = "SELECT * FROM hotels \
            WHERE (stars > ?) AND (stars < ?)\
              AND (price > ?) AND (price < ?)\
              AND (city = ?) LIMIT ? OFFSET ?"

            tupla1 = tuple([params[chave] for chave in params])
            result = cursor.execute(query1, tupla1)

        hotels = []
        for line in result:
            hotels.append({
                'hotel_id': line[0],
                'name': line[1],
                'stars': line[2],
                'price': line[3],
                'city': line[4]
            })

        #return {'hotels': [hotel.json() for hotel in HotelModel.query.all()]}
        return {'hotels': hotels}


class Hotel(Resource):
    args1 = reqparse.RequestParser()
    args1.add_argument('name',
                       type=str,
                       required=True,
                       help="the filed 'name' cant be left blank")
    args1.add_argument('stars',
                       type=float,
                       required=True,
                       help="the field stars cant be lef blank")
    args1.add_argument('price')
    args1.add_argument('city')

    # def find_hotel(hotel_id):
    #   for hotel in hoteis:
    #     if hotel_id == hotel['hotel_id']:
    #       return hotel
    #   return None

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message': 'Hotel Not Found.'}, 404

    ## o decorador a seguir garante que o post requer o login para ser feito
    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {
                "message": "Hotel id '{}' already exists.".format(hotel_id)
            }, 400  # bad request

        data = Hotel.args1.parse_args()
        hotel = HotelModel(hotel_id, **data)

        try:
            hotel.save_hotel()  ## save on db
            return hotel.json(), 200
        except:
            return {
                'message': 'An internal error occurrend trying to save hotel'
            }, 500

        # new_hotel=hotel.json()

        # hoteis.append(new_hotel)

    @jwt_required
    def put(self, hotel_id):
        data = Hotel.args1.parse_args()

        finded_hotel = HotelModel.find_hotel(hotel_id)
        if finded_hotel:
            finded_hotel.update_hotel(**data)
            try:
                hotel.save_hotel()  ## save on db
                return finded_hotel.json(), 200
            except:
                return {
                    'message':
                    'An internal error occurrend trying to save hotel'
                }, 500

        hotel = HotelModel(hotel_id, **data)

        try:
            hotel.save_hotel()  ## save on db
        except:
            return {
                'message': 'An internal error occurrend trying to save hotel'
            }, 500

        return hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {'message': 'Hotel deleted.'}
            except:
                return {
                    'message':
                    'An internal error occurrend trying to delete hotel'
                }, 500

        return {'message': 'HOtel not found'}, 404


### alguns comandos
'''
 ### POST: 
curl -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTY1NjI3MTksIm5iZiI6MTU5NjU2MjcxOSwianRpIjoiYjgwMjY0MGYtZDA1ZS00OTA0LWFkZWUtYTU2OTljZWIwYzIxIiwiZXhwIjoxNTk2NTYzNjE5LCJpZGVudGl0eSI6MiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.6_uSEe9hf3CSpKG01SL4yEgH2uaXkyveoOicfkSw_qY"\
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