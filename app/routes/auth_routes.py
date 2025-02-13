from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import User  # Import from the models package
from app.schemas.auth_schema import SignUpModel, SignUpResponse
from app.schemas.login import LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.get('/healthcheck')
async def healthcheck():
    return {"status": "ok"}


@auth_router.post('/signup', response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, session: Session = Depends(get_db)):
    # Check if email or username already exists
    db_email = session.query(User).filter(user.email == User.email).first()
    db_username = session.query(User).filter(
        user.username == User.username).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with the email already exists")
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with the username already exists")
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()

  # Return the user as a SignUpResponse model (matching the response_model)
    return SignUpResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        is_active=new_user.is_active,
        is_staff=new_user.is_staff
    )


@auth_router.post('/login')
async def login(user: LoginModel, session: Session = Depends(get_db), auth: AuthJWT = Depends()):
    db_user = session.query(User).filter(
        user.username == User.username).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists")
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = auth.create_access_token(subject=db_user.username)
        refresh_token = auth.create_refresh_token(subject=db_user.username)

        response = {
            'acces_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonable_encoder(response)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="username or password is wrong")

# refresh token


@auth_router.get('/refresh-token')
async def refresh_token(auth: AuthJWT = Depends()):

    try:
        auth.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you must send a refresh token  ")
    current_user = auth.get_jwt_subject()
    access_token = auth.create_access_token(subject=current_user)
    refresh_token = auth.create_refresh_token(subject=current_user)
    response = {
        'acces_token': access_token,
        'refresh_token': refresh_token
    }
    return jsonable_encoder(response)
