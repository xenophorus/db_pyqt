import os

from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path = os.getcwd()

print(path)

engine = create_engine(f'sqlite:///{path}/db/server.sql', echo=True, pool_recycle=7200)

Base = declarative_base()


class Users:
    __tablename__ = 'all_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    ip = Column(String(50))
    sock = Column(String)
    is_active = Boolean

    def __init__(self, username, user_hash, ip, v_port, is_active):
        self.username = username
        self.ip = ip
        self.v_port = v_port
        self.is_active = is_active


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


def db_user_add(user):
    name, ip, sock, is_active = user
    session.add(Users(name, ip, sock, is_active))
    session.commit()


def db_change_user_activity(id):
    session.query(Users).filter(Users.id == id).update({'is_active': False})
    session.commit()


def db_user_delete(id):
    session.query(Users).filter(Users.id == id).delete()
    session.commit()


def db_active_user():
    session.query(Users).filter(Users.is_active == True)
