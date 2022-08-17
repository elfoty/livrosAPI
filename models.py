from ast import AugStore
from sqlalchemy import Column, Integer, String
from database import Base

class Livros(Base):
    __tablename__="livro"

    id=Column(Integer, primary_key=True, index=True)
    titulo=Column(String)
    autor=Column(String)
    professor=Column(String)