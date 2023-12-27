from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "thegera4": {
        "username": "thegera4",
        "fullname": "Gerardo Medellin",
        "email": "thegera4@hotmail.com",
        "disabled": False,
        "password": "asdfg"
    },
    "sarina_next": {
        "username": "sarina_next",
        "fullname": "Amira Sarina",
        "email": "sarina_next@hotmail.com",
        "disabled": True,
        "password": "qwerty"
    },
}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])  # ** is used to unpack the dictionary
    else:
        return 0


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])  # ** is used to unpack the dictionary
    else:
        return 0


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if user == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.",
                            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user.")
    return user


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form_data.username)
    if user == 0:
        raise HTTPException(status_code=400, detail="Invalid username.")
    if not user.password == form_data.password:
        raise HTTPException(status_code=400, detail="Invalid password.")
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_me(user: User = Depends(current_user)):
    return user
