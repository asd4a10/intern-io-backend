from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.sessions import SessionMiddleware
import os
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Import database setup and User model from database.py
from database import User, get_db

# import authentication router
from auth.routes import auth_router

app = FastAPI()

# Add session middleware
app.add_middleware(
    SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY")  # Use a strong key
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])


# Pydantic schema for user input
class UserCreate(BaseModel):
    name: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "name": db_user.name}


@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User with id {user_id} deleted."}


@app.get("/users/", response_model=list[dict])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "name": user.name} for user in users]
