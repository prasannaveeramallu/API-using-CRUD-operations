from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException 
from models import User, Gender, Role, UserUpdateRequest
app = FastAPI()

db: List[User] = [User(id=UUID("e21d449e-de2c-4ec0-9b52-603ef4ee4a31"), first_name='Jennie', last_name='Robbins', middle_name='Ruby',
         gender=Gender.female, roles=[Role.admin]),
    User(id=UUID("72a7fecf-a761-4eb0-9986-016cdc9023fa"), first_name='Alex', last_name='Jacobs', middle_name='Ryan',
         gender=Gender.male, roles=[Role.student])     
]

@app.get('/')
async def root():
    return {'Hello' : 'World'}

@app.get('/users')
async def fetch_users():
    return db

@app.post('/users')
async def register_user(user:User):
    db.append(user)
    return {"user_id": user.id}

@app.delete('/users')
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return "User deleted"
    raise HTTPException(
        status_code=404,
        detail=f"user with the id: {user_id} does not exist"
    )    

@app.put('/users/{user_id}')
async def update_user(user_update: UserUpdateRequest, user_id:UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return "User updated"
    raise HTTPException(
        status_code=404, 
        detail=f"user with the id: {user_id} does not exist"
    )                    