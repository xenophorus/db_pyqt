import os
from sqlalchemy import *
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base


path = os.getcwd()


engine = create_engine(f'sqlite:///{path}\\..\\test.sql', echo=True, pool_recycle=7200)
res = engine.execute("select * from test_table")
print(res.fetchall())

# metadata = MetaData()

#
# alch_table = Table('alch_tbl', metadata,
#                    Column('id', Integer, primary_key=True),
#                    Column('name', String(50)),
#                    Column('fullname', String(50)),
#                    Column('password', String(50))
#                    )
#
# metadata.create_all(engine)
#
#
# class User:
#     def __init__(self, name, fullname, password):
#         self.name = name
#         self.fullname = fullname
#         self.password = password
#
#     def __repr__(self):
#         return f"<User({self.name}, {self.fullname}, {self.password})>"
#
#
# print(mapper(User, alch_table))
#
# user = User('Alex', 'Alexey', 'qwerty')
# print(user)

Base = declarative_base()


class User(Base):
    __tablename__ = 'alch_tbl'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ip = Column(String(100))
    sock = Column(String)
    is_active = Column(Binary)

    def __init__(self, name, ip, sock, is_active):
        self.name = name
        self.ip = ip
        self.sock = sock
        self.is_active = is_active

    def __repr__(self):
        return f'<User {self.name}, ip {self.ip}, active = {self.is_active}>'


alch_table = User.__table__
metadata = Base.metadata
# metadata.drop_all()
