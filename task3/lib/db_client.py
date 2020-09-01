import os
from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base


path = os.getcwd()

print(path)

engine = create_engine(f'sqlite:///{path}/db/client.sql', echo=True, pool_recycle=7200)

Base = declarative_base()


class Messages:
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    from_user = Column(String(50), ForeignKey('all_users.name'))
    to_user = Column(String(50), ForeignKey('all_users.name'))
    msg_time = Column(String(50))
    msg_text = Column(String)
    # ForeignKey

    def __init__(self, from_user, to_user, msg_time, msg_text):
        self.from_user = from_user
        self.to_user = to_user
        self.msg_time = msg_time
        self.msg_text = msg_text


