from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)) -> TicketRead:
    service = TicketService(TicketRepository(db), UserRepository(db))
    return service.create_ticket(payload)


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> TicketRead:
    service = TicketService(TicketRepository(db), UserRepository(db))
    return service.get_ticket(ticket_id)


@router.get("/", response_model=list[TicketRead])
def list_tickets(db: Session = Depends(get_db)) -> list[TicketRead]:
    service = TicketService(TicketRepository(db), UserRepository(db))
    return service.list_tickets()


@router.put("/{ticket_id}", response_model=TicketRead)
def update_ticket(
    ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)
) -> TicketRead:
    service = TicketService(TicketRepository(db), UserRepository(db))
    return service.update_ticket(ticket_id, payload)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)) -> None:
    service = TicketService(TicketRepository(db), UserRepository(db))
    service.delete_ticket(ticket_id)
    return None
