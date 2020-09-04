import os

from sqlalchemy import Column, Integer, String, Boolean, create_engine, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

path = os.getcwd()

print(path)

engine = create_engine(f'sqlite:///{path}/db/server.sql', echo=True, pool_recycle=7200)

Base = declarative_base()


# TODO Relationships between tables; https://docs.sqlalchemy.org/en/13/orm/tutorial.html

class Users:
    __tablename__ = 'all_users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    user_hash = Column(String(100), unique=True, nullable=False)
    ip = Column(String(50))
    is_active = Column(Boolean)

    users_log = relationship('UsersLog', backref='all_users', order_by='UsersLog.id')

    def __init__(self, username, user_hash, ip, is_active):
        self.username = username
        self.user_hash = user_hash
        self.ip = ip
        self.is_active = is_active


class UsersLog:
    __tablename__ = 'users_log'
    id = Column(Integer, primary_key=True)
    user_hash = Column(String(100), ForeignKey('all_users.user_hash'))
    time_conn = Column(DateTime)
    time_exit = Column(DateTime)

    all_users = relationship('Users', backref='users_log', order_by='Users.id')

    def __init__(self, user_hash, time_conn, time_exit):
        self.user_hash = user_hash
        self.time_conn = time_conn
        self.time_exit = time_exit


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


def db_user_add(user):
    name, user_hash, ip, is_active = user
    session.add(Users(name, user_hash, ip, is_active))
    session.commit()


def db_change_user_activity(user_hash):
    session.query(Users).filter(Users.id == user_hash).update({'is_active': False})
    session.commit()


def db_user_delete(user_hash):
    session.query(Users).filter(Users.id == user_hash).delete()
    session.commit()


def db_active_user():
    session.query(Users).filter(Users.is_active == True)
