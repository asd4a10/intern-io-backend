# auth/routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, User
from .oauth import oauth

from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

auth_router = APIRouter()


# Redirect to Google's OAuth 2.0 server
@auth_router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


# Handle the callback after Google authentication
@auth_router.get("/auth/callback", name="auth_callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token['userinfo']
    except Exception as e:
        raise HTTPException(status_code=400, detail="Authentication failed") from e
    
    # Extract user information
    print("user_info:", user_info)
    google_id = user_info["sub"]
    email = user_info["email"]
    name = user_info["name"]

    # Check if user exists
    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        # Create new user
        user = User(google_id=google_id, email=email, name=name)
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
    else:
        # Optionally update user info
        user.email = email
        user.name = name
        db.commit()

    # Implement session handling or token generation here

    return {
        "message": "Successfully authenticated",
        "user": {"id": user.id, "name": user.name},
    }
