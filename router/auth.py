from warnings import deprecated

from fastapi import APIRouter,status,Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext


router=APIRouter(prefix='/auth',tags=['auth'])
template=Jinja2Templates('templates')


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]
bcrypt_context=CryptContext(schemes='bcrypt',deprecated='auto')




def redirect_to_login():
    redirect_response=RedirectResponse(url='/auth/login',status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    return redirect_response
#----------------------------------------------PAGES--------------------------------------||

@router.get('/login',status_code=status.HTTP_200_OK)
async def login_page_for_normal(request:Request):
    return redirect_to_login()

@router.get('/register-page',status_code=status.HTTP_200_OK)
async def register_page(request:Request):
    return template.TemplateResponse('register.html',{'request':request})

#-----------------------------------------------ENDPOINTS---------------------------------||
class RegisterForm(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    password: str
    phone_number: str

@router.post('/register')
async def register_user(request:Request,regdata:RegisterForm,db:db_dependency):
    print("/register invoked")
    print(regdata.email)
    print(regdata.username)
    print(regdata.first_name)
    print(regdata.last_name)
    print(regdata.password)
    print(regdata.is_active)
    print(regdata.phone_number)
    print(regdata.role)
    hashed_password=bcrypt_context.hash(regdata.password)
    user_model=Users(username=regdata.username,
                     email=regdata.email,
                     first_name=regdata.first_name,
                     last_name=regdata.last_name,
                     hashed_password=hashed_password,
                     role=regdata.role,
                     is_active=regdata.is_active,
                     phone_number=regdata.phone_number
                     )
    db.add(user_model)
    db.commit()
    return False