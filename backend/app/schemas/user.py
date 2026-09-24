from datetime import datetime

from pydantic import BaseModel, EmailStr

#input gaurdrails 

class UserCreate(BaseModel):
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }