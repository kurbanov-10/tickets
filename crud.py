from sqlalchemy.orm import Session
import models, schemas, uuid 

def get_current_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=user.password + "notreallyhashed"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, username: str, password: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user and db_user.hashed_password == password + "notreallyhashed":
        return db_user
    return None

def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    ticket_code = str(uuid.uuid4())
    db_ticket = models.Ticket(
        customer_name=ticket.customer_name,
        event_name=ticket.event_name,
        ticket_code=ticket_code,
        is_used=False,
        user_id=ticket.user_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def use_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        db_ticket.is_used = True
        db.commit()
        db.refresh(db_ticket)
    return db_ticket