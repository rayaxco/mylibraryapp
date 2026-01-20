from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base, engine


class Users(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=True)
    hashed_password=Column(String)
    email=Column(String,unique=True)
    first_name=Column(String)
    last_name=Column(String)
    phone_number=Column(String)
    role=Column(String)
    is_active=Column(Boolean)

class Books(Base):
    __tablename__='books'
    id=Column(Integer,primary_key=True,index=True)
    bookname=Column(String,unique=True)
    author=Column(String)
    price=Column(Integer)
    genre=Column(String)
    summary=Column(String)
    uploader_id=Column(Integer,ForeignKey('users.id'))

class Cart(Base):
    __tablename__='cart'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    book_id=Column(Integer,ForeignKey('books.id'))

Base.metadata.create_all(bind=engine)
print('tables created successfully')