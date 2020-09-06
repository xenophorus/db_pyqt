import os
from _datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

path = os.getcwd()

engine = create_engine(f'sqlite:///{path}/db/db_server.sql', echo=False, pool_recycle=7200)

Base = declarative_base()


# TODO Relationships between tables; https://docs.sqlalchemy.org/en/13/orm/tutorial.html

class Users(Base):
    __tablename__ = 'all_users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50))
    user_hash = Column(String(100))
    ip = Column(String(50))
    is_active = Column(Boolean)

    users_log = relationship('UsersLog', backref='all_users', order_by='UsersLog.id')

    def __init__(self, username, user_hash, ip, is_active):
        self.username = username
        self.user_hash = user_hash
        self.ip = ip
        self.is_active = is_active


class UsersLog(Base):
    __tablename__ = 'users_log'
    id = Column(Integer, primary_key=True)
    user_hash = Column(String(100), ForeignKey('all_users.user_hash'))
    time_conn = Column(String(30))
    time_exit = Column(String(30))

    # all_users = relationship('Users', backref='users_log', order_by='Users.id')

    def __init__(self, user_hash, time_conn, time_exit):
        self.user_hash = user_hash
        self.time_conn = time_conn
        self.time_exit = time_exit


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


def db_user_add(user):
    name, u_id, u_ip, is_active = user
    a = Users(name, u_id, u_ip, is_active)
    b = UsersLog(u_id, datetime.today().isoformat(), '')
    session.add(a)
    session.add(b)
    session.commit()


def db_change_user_activity(ip):
    session.query(Users).filter(Users.ip == ip).update({'is_active': False})
    session.commit()


def db_user_delete(username):
    session.query(Users).filter(Users.id == username).delete()
    session.commit()


def db_active_users():
    userlist = session.query(Users).filter(Users.is_active == True).filter(Users.username)
    return userlist


def db_user_in(name):
    for n in session.query(Users).filter(Users.username):
        if n == name:
            return True
        else:
            return False


def db_user_ip(name):
    try:
        a = session.query(Users).filter(Users.username == name).first()
        return a.ip
    except AttributeError:
        return None


# z = db_user_ip('Sarah')
# print(z)
