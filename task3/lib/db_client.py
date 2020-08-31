import os
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base


path = os.getcwd()

print(path)

engine = create_engine(f'sqlite:///{path}/../db/client.sql', echo=True, pool_recycle=7200)

Base = declarative_base()


class Messages:
    pass

