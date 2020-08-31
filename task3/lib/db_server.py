import os

from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


path = os.getcwd()

engine = create_engine(f'sqlite:///{path}/../db/server.sql', echo=True, pool_recycle=7200)

Base = declarative_base()


class Users:
    __tablename__ = 'all_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    ip = Column(String(50))
    sock = Column(String)
    is_active = Boolean

    def __init__(self, username, ip, v_port, is_active):
        self.username = username
        self.ip = ip
        self.v_port = v_port
        self.is_active = is_active


def add_user(tpl):
    user = Users(*tpl)
    session.add(user)
    session.commit()


def mod_user(sock):
    session.query(Users).filter(sock)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


