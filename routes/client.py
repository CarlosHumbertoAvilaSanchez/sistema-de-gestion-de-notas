from fastapi import APIRouter, HTTPException

from config.db import Session
from models.client import Client
from schemas.client import ClientSchema

client_router = APIRouter(prefix="/clients", tags=["Client"])


@client_router.get("")
async def get_clients():
    try:
        with Session() as session:
            clients = session.query(Client).limit(10).all()
            if not clients:
                raise HTTPException(status_code=404, detail="Clients not found")
            return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@client_router.get("/{client_id}")
async def get_client(client_id: int):
    try:
        with Session() as session:
            client = session.query(Client).filter(Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@client_router.post("", response_model=ClientSchema)
async def create_client(client: ClientSchema):
    try:
        with Session() as session:
            if validate_client(client):
                new_client = Client(
                    first_name=client.first_name,
                    last_name=client.last_name,
                    phone=client.phone,
                )

                session.add(new_client)
                session.commit()
                session.refresh(new_client)
                return new_client

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def validate_client(client: ClientSchema):
    with Session() as session:
        client_exists = (
            session.query(Client).filter(Client.phone == client.phone).first()
        )
        if client_exists:
            raise HTTPException(status_code=400, detail="Client already registered")

        return True


@client_router.put("/{client_id}", response_model=ClientSchema)
async def update_client(client_id: int, client: ClientSchema):
    try:
        with Session() as session:
            client_to_update = (
                session.query(Client).filter(Client.client_id == client_id).first()
            )
            if not client_to_update:
                raise HTTPException(status_code=404, detail="Client not found")

            client_to_update.first_name = client.first_name
            client_to_update.last_name = client.last_name
            client_to_update.phone = client.phone
            session.commit()
            session.refresh(client_to_update)
            return client_to_update

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@client_router.delete("/{client_id}")
async def delete_client(client_id: int):
    try:
        with Session() as session:
            client = session.query(Client).filter(Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            session.delete(client)
            session.commit()
            return {"message": "Client deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
