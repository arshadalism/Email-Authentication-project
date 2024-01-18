import random
from fastapi import FastAPI, HTTPException
import uvicorn
import db
import schema
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Email Authentication")


@app.post("/signup")
async def signup(signup_data: schema.User_signup_data):
    response = await db.user_signup(signup_data)
    if response:
        token = response["token"]
        result = await send_verification_email(signup_data.email, token)
        return result
    else:
        raise HTTPException(status_code=404, detail="No data found.")


async def send_verification_email(email: str, token: str):
    otp = random.randint(000000, 999999)
    try:
        await db.otp_data(email, otp)
    except Exception as e:
        print(f"Error saving otp in the database:{e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    message = Mail(from_email="chaudharyarshad548@gmail.com",
                   to_emails=email,
                   subject="Email verification code",
                   plain_text_content=f"Use the code to verify the email: {otp}",
                   html_content=f"<p>Use the code to verify your email: <strong>{otp}</strong></p>")
    try:
        api_key = os.getenv("API_KEY")
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        return {"message": "Email verification code send successfully", "response": response}
    except Exception as e:
        print(e)
        return {"message": e}


@app.post("/verify_email")
async def verify_email(email_data: schema.Email_verification):
    response = await db.otp_col.find_one({"otp": email_data.otp})
    if response:
        await db.signup_col.find_one_and_update({"email": email_data.email}, {"$set": {"active": True}})
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=404, detail=f"No user found with this {email_data.email}")


@app.post("/login")
async def login(login_data: schema.Login_data):
    # hashed_password = pwd_context.hash(login_data.password)
    # print(login_data.username)
    # print(hashed_password)
    data = await db.signup_col.find_one({"username": login_data.username, "active": True})
    if data:
        return {"message": f"Login successfully with the username {login_data.username}"}
    return {"message": "Email is not verified.Please verify the email first."}


if __name__ == '__main__':
    uvicorn.run("main:app")
