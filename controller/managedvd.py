import jwt
import json as js
from db.connectdb import get_db_session
from main import * 
from sanic import Blueprint, text
from models.dvd_model import *
from sanic.response import json
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select
from uuid import UUID

managedvd = Blueprint("managedvd", url_prefix="/dvd")
engine = create_async_engine("mysql+aiomysql://root@localhost:3306/nefos23dvd", echo=True)

def is_valid_enum_value(input_str):
    for member in EidosEnum:
        if member.value == input_str:
            return True
    return False

@managedvd.get("/")
async def get_dvd(request):
    #get the session to the db
    Session = async_sessionmaker(engine,  expire_on_commit = False)
    async with Session.begin() as session:
        result = (await session.execute(select(DVD)))
        json_data_list = [];
        results = [row[0].to_dict() for row in result]
        for res in results :
            print(res)
        json_string = js.dumps(results)
        # for dvd in result.fetchall():
        #     json_data_list.append(dvd);

        return text(json_string)


@managedvd.get("/<dvd_info:str>")
async def get_dvdid(request, dvd_info: str):
    #get the session to the db
    Session = async_sessionmaker(engine,  expire_on_commit = False)
    async with Session.begin() as session:
        dvd = (await session.scalars(select(DVD).where(DVD.id == dvd_info))).one_or_none()
        if dvd is None:
            dvd = (await session.scalars(select(DVD).where(DVD.titlos == dvd_info))).one_or_none()
            if dvd is None:
                return json({"error": "dvd with that info not found"}, status=404)
            
        
        return json((dvd.to_dict()), status=200)

@managedvd.delete("/<dvd_id:str>")
async def delete_dvdid(request, dvd_id: str):
    Session = async_sessionmaker(engine,  expire_on_commit = False)
    async with Session.begin() as session:
        dvd = (await session.scalars(select(DVD).where(DVD.id == dvd_id))).one_or_none()
        
        if dvd is None :
            return json({"error": "dvd with that id not found"}, status=404)
        
        row = await session.execute(select(DVD).where(DVD.id == dvd_id))
        row = row.scalar_one()
        await session.delete(row)
        await session.commit()

        #return a response
        return json("to dvd diagraftike", status=200)

@managedvd.patch("/<dvd_id:str>")
async def updateDvd(request, dvd_id: str):
    dvdjson = request.json #get the json from the request
    if not "temaxia" in dvdjson and not "eidos" in dvdjson:
        return json({"error": "Lathos eisagwgi stoixeiwn"}, status=400)

    Session = async_sessionmaker(engine,  expire_on_commit = False)
    async with Session.begin() as session:
        if "temaxia" in dvdjson:
            dvd = (await session.scalars(select(DVD).where(DVD.id == dvd_id))).one_or_none()
            if isinstance(dvdjson["temaxia"], int):
                dvd.temaxia = dvdjson["temaxia"]
                session.add(dvd)
                await session.commit()
            else:
                return json("lathos temaxia", status=400)

        elif "eidos" in dvdjson:
            dvd = (await session.scalars(select(DVD).where(DVD.id == dvd_id))).one_or_none()
            if not is_valid_enum_value(dvdjson["eidos"]):
                return json({"error": "lathos eidos dvd"}, status=400)
    
            dvd.eidos = dvdjson["eidos"]
            session.add(dvd)
            await session.commit()
        
        return json("to dvd allaxe", status=200)

@managedvd.post("/")
async def create_dvd(request):
    dvdjson = request.json #get the json from the request

    if not "temaxia" in dvdjson:
        return json({"error": "temaxia is mandatory"}, status=400)
    if not "eidos" in dvdjson:
        return json({"error": "eidos is mandatory"}, status=400)
    if not "titlos" in dvdjson:
        return json({"error": "titlos is mandatory"}, status=400)
    
    dvd = DVD(**dvdjson) #unpack json to a dvd object

    if dvd.temaxia <= 0:
        return json({"error": "lathos plithos temaxiwn"}, status=400)
    
    if not is_valid_enum_value(dvd.eidos):
        return json({"error": "lathos eidos dvd"}, status=400)

    
    #get the session to the db
    Session = async_sessionmaker(engine,  expire_on_commit = False)
    async with Session.begin() as session:
        returned_dvd = (await session.execute(select(DVD).where(DVD.titlos == dvd.titlos))).one_or_none()
    
        if returned_dvd is not None :
            return  json({"error": "title already exists"}, status=400)
        
        session.add(dvd)
        await session.commit()
    
        #return a response
        return json((dvd.to_dict2()), status=200)
   