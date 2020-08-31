import os
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


path = os.getcwd()


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


user1 = User('Olga', '192.168.1.31', '', True)
user2 = User('Alex', '192.168.1.32', '', True)
user3 = User('Dan', '192.168.1.33', '', True)
user4 = User('Nastya', '192.168.1.34', '', True)
user5 = User('Helen', '192.168.1.35', '', True)

session.add_all([user1, user2, user3, user4, user5])

session.commit()

# print(user2.id)
# user4.is_active = False

# for ins in session.query(User):
#     print(ins)
#
# print(session.query(User))

# session.flush()
a = session.query(User).filter(User.ip == '192.168.1.35')
for i in a:
    print(i.ip)
# session.query(User).filter(User.ip == '192.168.1.35').delete()
session.commit()
