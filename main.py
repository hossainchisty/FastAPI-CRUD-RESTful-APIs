from fastapi import FastAPI
from fastapi import status
from typing import Optional, List
from sqlmodel import Session, select
from fastapi.exceptions import HTTPException

from models import Hero
from models import engine

app = FastAPI()

session = Session(bind=engine)

@app.get("/")
async def read_main():
    return {"msg": "Hello FastAPI!"}



# Get ---> http://localhost:8000/
@app.get('/heros', response_model=List[Hero], status_code=status.HTTP_200_OK)
async def get_all_hero():
    ''' Get all heros '''
    statement = select(Hero)
    results = session.exec(statement).all()
    return results

@app.get('/heros/{hero_id}',response_model=Hero, status_code=status.HTTP_200_OK)
async def get_a_hero(hero_id: int):
    ''' Get a hero '''
    statement = select(Hero).where(Hero.id == hero_id)
    print(statement)
    result = session.exec(statement).first()
    
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")

    return result

# Post ---> http://localhost:8000/create/heros/
@app.post('/create/heros/', response_model=Hero)
async def create_new_heros(hero:Hero):
    ''' Create a new hero '''
    statement = Hero(name=hero.name,secret_name=hero.secret_name,age=hero.age)

    session.add(statement)
    session.commit()

    return {"message": "Hero created successfully", "hero": statement, "status": status.HTTP_201_CREATED}

# Put ---> http://localhost:8000/heros/{hero_id}/update/

@app.put('/heros/{hero_id}/update/',response_model=Hero)
async def update_hero_model(hero_id:int,hero:Hero):
    statement=select(Hero).where(Hero.id==hero_id)

    result=session.exec(statement).first()
 
    result.name=hero.name
    result.secret_name=hero.secret_name
    result.age=hero.age

    session.commit()

    return {"message": "Hero updated successfully", "hero": result}


# Delete ---> http://localhost:8000
@app.delete('/heros/{hero_id}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_heros(hero_id: int):
    ''' Delete a hero '''
    statement = select(Hero).where(Hero.id == hero_id)
    result = session.exec(statement).first()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")

    else:
        session.delete(result)
        session.commit()

    return {"message": "Hero deleted successfully", "status": status.HTTP_204_NO_CONTENT,}