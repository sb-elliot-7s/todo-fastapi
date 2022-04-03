from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(min_length=6)


class UserSchema(CreateUserSchema):
    id: int

    class Config:
        orm_mode = True


class JWTTokenSchema(BaseModel):
    access_token: str
    token_type: str
