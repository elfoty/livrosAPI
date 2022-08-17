from concurrent.futures.process import BrokenProcessPool
import imp
import string
from typing import final
from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Livro(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    professor: str = Field(min_length=1)

LIVROS = []

@app.post("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Livros).all()

@app.post("/cadastro-livro")
def cadastro(livro: Livro, db: Session = Depends(get_db)):
    book_model = models.Livros()
    book_model.titulo = livro.titulo
    book_model.autor = livro.autor
    book_model.professor = livro.professor

    db.add(book_model)
    db.commit()
    return livro

@app.put("/{book_id}")
def update_book(book_id: int, book: Livro, db: Session = Depends(get_db)):
    
    book_model = db.query(models.Livros).filter(models.Livros.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        ) 

    book_model.titulo = book.titulo
    book_model.autor = book.autor
    book_model.professor = book.professor
    db.add(book_model)
    db.commit()
    return book