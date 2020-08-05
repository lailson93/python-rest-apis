from sql_alchemy import database1

class UserModel(database1.Model):

############################### Parte para entender é uma tabela ######
  __tablename__ = 'users'

  user_id = database1.Column(database1.Integer, primary_key=True)
  login = database1.Column(database1.String(40))
  password = database1.Column(database1.String(40))

######################################################################
  def __init__(self, login, password):
    self.login = login
    self.password = password

  def json(self):
    return {
      'user_id': self.user_id,
      'login': self.login
    }

  @classmethod
  def find_user(cls, user_id): ## pq ele nao acessa nada relacionado ao self
    user = cls.query.filter_by(user_id=user_id).first() ## SELECT * FROM hotels WHERE hotel_id = hotel_id LIMIT 1
    if user:
      return user
    return None
    
  @classmethod
  def find_by_login(cls, login): ## pq ele nao acessa nada relacionado ao self
    user = cls.query.filter_by(login=login).first() ## SELECT * FROM hotels WHERE hotel_id = hotel_id LIMIT 1
    if user:
      return user
    return None

  def save_user(self):
    database1.session.add(self) ## add o proprio objeto ao banco
    database1.session.commit()

  def delete_user(self):
    database1.session.delete(self)
    database1.session.commit()
