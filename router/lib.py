from tokenize import cookie_re
from typing import Annotated

from fastapi import Request,APIRouter,status,HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import SessionLocal
from pydantic import BaseModel

from models import Users
from fastapi.templating import Jinja2Templates
from router.auth import get_current_user
from models import Books

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]

router=APIRouter(prefix='/lib',tags=['lib'])

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
templates=Jinja2Templates('templates')
# ---------------------------------------------------------REDIRECTS------------------------------------------------


def redirect_to_login():
    redirect_response=RedirectResponse(url='/auth/login',status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    return redirect_response

def redirect_to_home():
    redirect_response=RedirectResponse(url='/lib/home',status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    return redirect_response

# ---------------------------------------------------------PAGES------------------------------------------------



@router.get('/home',status_code=status.HTTP_302_FOUND)
async def home_page(request:Request,db:db_dependency):

    token=request.cookies.get('access_token')
    user=get_current_user(token)
    if user is None:
        return redirect_to_login()
    # print(user.get('username'))
    # print(user.get('id'))
    # print(user.get('role'))
    books_raw=db.query(Books).all()
    books=[]
    for book in books_raw:
        combined_bookname_author=str(book.bookname+book.author+'.png')
        image_link=combined_bookname_author.replace(" ","")
        books.append({'id':book.id,
                      'bookname':book.bookname,
                      'author':book.author,
                      'price':book.price,
                      'genre':book.genre,
                      'summary':book.summary,
                      'image_url':image_link})

    return templates.TemplateResponse('home.html',{'request':request,'user':user,'books':books})

@router.get('/admin-actions')
async def admin_action_page(db:db_dependency,request:Request):
    try:
        user=get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        if user.get('role') == 'admin':
            return templates.TemplateResponse('admin-actions.html',{'request':request,'user':user})
        return redirect_to_home()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Could not verify')

@router.get('/show-users')
async def show_all_users(request:Request,db:db_dependency):
    try:
        user=get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        if user.get('role') == 'admin':
            # all_users=db.query(Users.id,Users.username,Users.email,Users.first_name,Users.last_name,Users.phone_number,Users.role,Users.is_active).all()
            all_users=db.query(Users).all()
            print('all ok')
            return templates.TemplateResponse('show-users.html',{'request':request,'user':user,'all_users':all_users})
        return redirect_to_home()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Could not verify')

@router.get('/show-books')
async def show_all_books(request:Request,db:db_dependency):
    try:
        user=get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        if user.get('role') == 'admin':
            # all_users=db.query(Users.id,Users.username,Users.email,Users.first_name,Users.last_name,Users.phone_number,Users.role,Users.is_active).all()
            all_books=db.query(Books).all()
            print('all ok')
            return templates.TemplateResponse('show-books.html',{'request':request,'user':user,'all_books':all_books})
        return redirect_to_home()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Could not verify')

#@router.get('/add-book')






#---------------------------------------------------------ENDPOINTS--------------------------------------------------||



# ---------------------------------------------------------FUNCTIONS-------------------------------------------------||


# INSERT INTO books (bookname, author, price, genre,summary,uploader_id) VALUES ('brain', 'robin cook', 500,'horror','brains in a hospital go missing',2);
# INSERT INTO books (bookname, author, price, genre,summary,uploader_id) VALUES ('one shot', 'lee child', 600,'crime thriller','4 people are shot by an unknown sniper',2);