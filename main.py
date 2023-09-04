from db.connectdb import init_db
from sanic import Sanic, Request, json
from sanic.response import text 
from sanic_auth import Auth
from login import login 
from auth import protected
from sanic_ext import Extend 
from models.dvd_model import *
import asyncio

from controller.managedvd import * 

app = Sanic("NefosApp")
app.config.SECRET = "login"
app.blueprint(login)
app.blueprint(managedvd)

@app.get("/")
async def hello(request):
    return text("Hello")

@app.get("/secret")
@protected
async def secret(request):
    return text("Hooray!")


init_db()