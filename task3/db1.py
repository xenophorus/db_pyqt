import os
from sqlalchemy import Column, Integer, String, Boolean, create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


path = os.getcwd()

print(path)


engine = create_engine(f'sqlite:///{path}/test.sql', echo=False, pool_recycle=7200)
# res = engine.execute("select * from test_table")
# print(res.fetchall())


Base = declarative_base()


class User(Base):
    __tablename__ = 'alch_tbl'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ip = Column(String(100))
    sock = Column(String)
    is_active = Column(Boolean)

    def __init__(self, name, ip, sock, is_active):
        self.name = name
        self.ip = ip
        self.sock = sock
        self.is_active = is_active

    def __repr__(self):
        return f'<User {self.name}, ip {self.ip}, active = {self.is_active}>'


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


def db_user_add(user):
    name, ip, sock, is_active = user
    session.add(User(name, ip, sock, is_active))
    session.commit()


def db_change_use_activity(id):
    session.query(User).filter(User.id == id).update({'is_active': False})
    session.commit()


def db_user_delete(id):
    session.query(User).filter(User.id == id).delete()
    session.commit()



db_user_add(('Carina', '192.168.2.31', '', True))
db_user_add(('Ann', '192.168.1.32', '', True))
db_user_add(('Lynda', '192.168.1.32', '', True))
db_user_add(('Jake', '192.168.1.32', '', True))
db_user_add(('Timothy', '192.168.1.32', '', True))


db_user_delete(22)


db_change_use_activity(29)


a = session.query(User)
for i in a:
    print(i)

