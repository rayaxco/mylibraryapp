from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from router import auth,lib
import models
from database import engine
from fastapi.staticfiles import StaticFiles
models.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(auth.router)
app.include_router(lib.router)

app.mount('/static',StaticFiles(directory="static"),name='static')

@app.get('/')
async def redirect_to_home():
    redirect_response=RedirectResponse('/lib/home',status_code=307)
    return redirect_response


