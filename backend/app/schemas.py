from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_admin: bool


class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    quantity: int

    class Config:
        from_attributes = True

class RestockPayload(BaseModel):
    quantity: int
