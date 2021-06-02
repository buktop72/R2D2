import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.operators import exists

Base = declarative_base()

engine = sq.create_engine('путь к БД')
Session = sessionmaker(bind=engine)
session = Session()


# Таблица с данными пользователя
class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    range_age = sq.Column(sq.String)
    city = sq.Column(sq.String)



# Таблица подобранных пар
class DatingUser(Base):
    __tablename__ = 'datinguser'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)       # id юзера-половинки
    first_name = sq.Column(sq.String)   # имя
    last_name = sq.Column(sq.String)    # фамилия
    id_User = sq.Column(sq.Integer, sq.ForeignKey('user.id')) # 
    user = relationship(User)


# Создать пустые таблицы в БД 
def create_tables():
    Base.metadata.create_all(engine)


# Добавляем пользователя в БД
def add_user(user):
    session.expire_on_commit = False
    session.add(user)
    session.commit()



# Показать пары из БД
def view_all(user_id):
    links = []
    id_query = session.query(User.id).order_by(User.id.desc()).filter(User.vk_id == user_id).limit(1)
    id_list = [p.id for p in id_query]
    id_user = id_list[0]
    dating_users_query = session.query(DatingUser.vk_id).filter(DatingUser.id_User == id_user).all()
    dating_users_list = [du.vk_id for du in dating_users_query]
    for link in dating_users_list:
        links.append(link)
    return links

