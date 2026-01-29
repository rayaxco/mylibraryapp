from warnings import deprecated

from fastapi import APIRouter,status,Request,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends
from passlib.exc import InvalidTokenError
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import timezone,timedelta,datetime

SECRET_KEY='81ec26f9d526fac4e9d77e2de38078c3aa8c5ccc2fac21c5ec0648cd9b320192'
ALGORITHM='HS256'


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





#----------------------------------------------PAGES--------------------------------------||

@router.get('/register-page',status_code=status.HTTP_200_OK)
async def register_page(request:Request):
    return template.TemplateResponse('register.html',{'request':request})

@router.get('/login',status_code=status.HTTP_200_OK)
async def register_page(request:Request):
    return template.TemplateResponse('login.html',{'request':request})

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
    print('pushed user: ',regdata.username,' to db.users..')
    return status.HTTP_201_CREATED




class LoginForm(BaseModel):
    username:str
    password:str
@router.post('/token')
async def create_token(loginform:LoginForm,db:db_dependency,request:Request):
    authenticated = authenticate(loginform.username, loginform.password, db)
    print(authenticated.get('username'))
    if authenticated:
        token=create_access_token(authenticated.get('username'),authenticated.get('id'),authenticated.get('role'),timedelta(minutes=20))
        print(token)
        return {'access_token':token,'token_type':'bearer'}


#----------------------------------------FUNCTIONS--------------------------------------||
def redirect_to_login():
    redirect_response=RedirectResponse(url='/auth/login',status_code=status.HTTP_200_OK)
    return redirect_response


def authenticate(username,password,db):
    user_model=db.query(Users).filter(Users.username==username).first()
    if user_model:
        password_matched=bcrypt_context.verify(password,user_model.hashed_password)
        if password_matched is True:
            return {'username':user_model.username,'id':user_model.id,'role':user_model.role}
    print('bad authentication.. Redirecting to login')
    return redirect_to_login()

def create_access_token(username,id,role,delta:timedelta):
    encode={'sub':username,'id':id,'role':role}
    expires=datetime.now(timezone.utc)+delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,ALGORITHM)


# @router.post('/token-decode')
def get_current_user(jtoken:str):
    try:
        user=jwt.decode(jtoken,key=SECRET_KEY,algorithms=ALGORITHM)
        username=user.get('sub')
        user_id=user.get('id')
        role=user.get('role')
        return {'username':username,'id':user_id,'role':role}
    except ExpiredSignatureError:
        print("Token has expired")
        redirect_to_login()
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Token invalid')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid token')
