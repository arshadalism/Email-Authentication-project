import uuid
import schema
from db_client import database
import random
import secrets
from passlib.context import CryptContext

Secret_key = secrets.token_hex(32)
ACCESS_TOKEN_EXPIRE_TIME = 5
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


signup_col = database.get_collection("Signup data")
otp_col = database.get_collection("otp collection")


async def user_signup(user_signup_data: schema.User_signup_data):
    hashed_password = pwd_context.hash(user_signup_data.password)
    token = str(uuid.uuid4())
    signup_data = {
        "_id": random.randint(1000, 99999),
        "username": user_signup_data.username,
        "email": user_signup_data.email,
        "password": hashed_password,
        "token": token,
        "active": False
    }
    await signup_col.insert_one(signup_data)
    return {"message": "success", "token": token}


async def otp_data(email, otp):
    await otp_col.insert_one({
        "_id": random.randint(1000, 99999),
        "email": email,
        "otp": otp
    })
    return {"message": "otp saved successfully"}
