from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship
from database import Base 

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    event_name = Column(String)
    ticket_code = Column(String, unique=True)
    is_used = Column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))   
    user: Mapped['User'] = relationship(back_populates='tickets')
      
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    first_name: Mapped[str] = mapped_column(String(length=100))
    last_name: Mapped[str] = mapped_column(String(length=100))
    hashed_password: Mapped[str] = mapped_column(String(length=200))
    
    tickets: Mapped['Ticket'] = relationship(back_populates='user',
                                         cascade='all, delete-orphan')
