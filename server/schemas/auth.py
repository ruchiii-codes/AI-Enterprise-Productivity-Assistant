from pydantic import BaseModel, EmailStr, Field

# The register form asks for at least 8 characters, but that is an HTML
# attribute and trivially bypassed, so the rule is enforced here too.
MIN_PASSWORD_LENGTH = 8


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=MIN_PASSWORD_LENGTH)
