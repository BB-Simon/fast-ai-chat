from pydantic import BaseModel, EmailStr, field_validator
import re

class SignupRequest(BaseModel):
  email: EmailStr
  password: str

  @field_validator("password")
  def validate_password(cls, val):
    if len(val) < 8:
      raise ValueError("Password must be at lest 8 charecters")
    
    if not re.search(r"[A-Z]", val):
      raise ValueError("Password must inclue uppercase letter")
    
    if not re.search(r"[a-z]", val):
      raise ValueError("Password must include lowarecase letter")
    
    if not re.search(r"0-9", val):
      raise ValueError("Password must include a number")
    
    return val


class LoginRequest(BaseModel):
  email: EmailStr
  password: str