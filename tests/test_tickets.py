import pytest


@pytest.mark.asyncio
async def test_create_ticket(client):
    user_resp = await client.post(
        "/users/",
        json={"name": "Ada", "email": "ada@example.com"},
    )
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    ticket_resp = await client.post(
        "/tickets/",
        json={
            "author_id": user_id,
            "title": "Bug",
            "description": "Something broken",
            "tags": ["backend", "urgent"],
        },
    )
    assert ticket_resp.status_code == 201
    body = ticket_resp.json()
    assert body["author_id"] == user_id
    assert body["tags"] == ["backend", "urgent"]
