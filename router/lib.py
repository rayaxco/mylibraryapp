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

# ---------------------------------------------------------PAGES------------------------------------------------



@router.get('/home',status_code=status.HTTP_302_FOUND)
async def home_page(request:Request,db:db_dependency):
    token=request.cookies.get('access_token')
    user=get_current_user(token)
    if user is None:
        redirect_to_login()
    books=db.query(Books).all()
    return templates.TemplateResponse('home.html',{'request':request,'user':user,'books':books})



#---------------------------------------------------------ENDPOINTS--------------------------------------------------||

# ---------------------------------------------------------FUNCTIONS-------------------------------------------------||


# INSERT INTO books (bookname, author, price, genre,summary,uploader_id) VALUES ('brain', 'robin cook', 500,'horror','brains in a hospital go missing',2);
# INSERT INTO books (bookname, author, price, genre,summary,uploader_id) VALUES ('one shot', 'lee child', 600,'crime thriller','4 people are shot by an unknown sniper',2);