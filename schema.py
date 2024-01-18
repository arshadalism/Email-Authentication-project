from pydantic import BaseModel, EmailStr


class User_signup_data(BaseModel):
    username: str
    email: EmailStr
    password: str


class Email_verification(BaseModel):
    email: str
    otp: int


class Login_data(BaseModel):
    username: str
    password: str


