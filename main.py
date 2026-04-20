from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select  
from models import User
import models, schemas, crud, database 

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Smart Ticket System")

@app.post("/tickets/", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    stmt = select(User).where(User.id == ticket.user_id)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(status_code=404, detail=f"{ticket.user_id}-raqamli user mavjud emas")

    return crud.create_ticket(db=db, ticket=ticket)

@app.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Chipta topilmadi")
    return db_ticket

@app.put("/tickets/{ticket_id}/use")
def mark_ticket_used(ticket_id: int, db: Session = Depends(database.get_db)):
    return crud.use_ticket(db=db, ticket_id=ticket_id)

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)
@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(database.get_db)):
    user = crud.login_user(db, username=username, password=password)
    if not user:
        raise HTTPException(status_code=404, detail="Noto'g'ri foydalanuvchi nomi yoki parol")
    return {"message": "Muvaffaqiyatli kirildi", "user_id": user.id}