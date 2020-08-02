from sql_alchemy import database1

class HotelModel(database1.Model):

  __tablename__ = 'hotels'

  hotel_id = database1.Column(database1.String, primary_key=True)
  name = database1.Column(database1.String(80))
  stars = database1.Column(database1.Float(precision=1))
  price = database1.Column(database1.Float(precision=2))
  city = database1.Column(database1.String(40))


  def __init__(self, hotel_id, name, stars, price, city):
    self.hotel_id = hotel_id
    self.name = name
    self.stars = stars
    self.price = price
    self.city = city

  def json(self):
    return {
      'hotel_id': self.hotel_id,
      'name': self.name,
      'stars': self.stars,
      'price': self.price,
      'city': self.city
    }

  @classmethod
  def find_hotel(cls, hotel_id): ## pq ele nao acessa nada relacionado ao self
    hotel = cls.query.filter_by(hotel_id=hotel_id).first() ## SELECT * FROM hotels WHERE hotel_id = hotel_id LIMIT 1
    if hotel:
      return hotel
    return None

  def save_hotel(self):
    database1.session.add(self) ## add o proprio objeto ao banco
    database1.session.commit()

  def update_hotel(self, name, stars, price, city):
    self.name = name
    self.stars = stars
    self.price = price
    self.city = city

  def delete_hotel(self):
    database1.session.delete(self)
    database1.session.commit()
