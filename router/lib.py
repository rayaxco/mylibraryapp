from tokenize import cookie_re
from typing import Annotated

from fastapi import Request,APIRouter,status
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import SessionLocal
from pydantic import BaseModel

from models import Users
from fastapi.templating import Jinja2Templates


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]

router=APIRouter(prefix='/lib',tags=['lib'])

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
# ---------------------------------------------------------REDIRECTS------------------------------------------------


def redirect_to_login():
    redirect_response=RedirectResponse(url='/auth/login',status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    return redirect_response

# ---------------------------------------------------------PAGES------------------------------------------------



@router.get('/home',status_code=status.HTTP_302_FOUND)
async def home_page(request:Request):
    return True

@router.get('/login',status_code=status.HTTP_200_OK)
async def login_for_normal(request:Request):
    pass



#---------------------------------------------------------ENDPOINTS------------------------------------------------
class User_Login(BaseModel):
    username:str
    password:str
@router.get('/token')
async def create_token(userlogin:User_Login,request: Request,db:db_dependency):
    authenticated=authenticate(userlogin.username,userlogin.password,db)
# ---------------------------------------------------------FUNCTIONS-------------------------------------------------
def authenticate(username,password,db):
    user_model=db.query(Users).filter(Users.username==username).first()
    if user_model:
        password_matched=bcrypt_context.verify(password,user_model.hashed_password)
        if password_matched is True:
            return True
    return False


