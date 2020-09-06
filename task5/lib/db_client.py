import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


path = os.getcwd()

print(path)

engine = create_engine(f'sqlite:///{path}/db/db_client.sql', echo=True, pool_recycle=7200)

Base = declarative_base()


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    from_user = Column(String(50))
    to_user = Column(String(50))
    msg_time = Column(String(50))
    msg_text = Column(String)

    def __init__(self, from_user, to_user, msg_time, msg_text):
        self.from_user = from_user
        self.to_user = to_user
        self.msg_time = msg_time
        self.msg_text = msg_text


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


def db_add_message(from_user, to_user, time, text):
    msg = Messages(from_user, to_user, time, text)
    session.add(msg)
    session.commit()
