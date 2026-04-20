from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    customer_name: str
    event_name: str
    user_id:int

class TicketResponse(TicketCreate):
    id: int
    ticket_code: str
    is_used: bool

    class Config:
        from_attributes = True
        
        
class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)


class UserCreate(UserBase):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)

class UserOut(UserBase):
    id: int

