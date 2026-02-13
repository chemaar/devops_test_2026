from fastapi import HTTPException, status

from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    def __init__(self, repo: TicketRepository, user_repo: UserRepository) -> None:
        self.repo = repo
        self.user_repo = user_repo

    def create_ticket(self, payload: TicketCreate) -> Ticket:
        if not self.user_repo.get_by_id(payload.author_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        ticket = Ticket(
            author_id=payload.author_id,
            title=payload.title,
            description=payload.description,
            tags=payload.tags,
        )
        return self.repo.create(ticket)

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
        return ticket

    def list_tickets(self) -> list[Ticket]:
        return self.repo.list()

    def update_ticket(self, ticket_id: int, payload: TicketUpdate) -> Ticket:
        ticket = self.get_ticket(ticket_id)
        if payload.title is not None:
            ticket.title = payload.title
        if payload.description is not None:
            ticket.description = payload.description
        if payload.tags is not None:
            ticket.tags = payload.tags
        return self.repo.update(ticket)

    def delete_ticket(self, ticket_id: int) -> None:
        ticket = self.get_ticket(ticket_id)
        self.repo.delete(ticket)
