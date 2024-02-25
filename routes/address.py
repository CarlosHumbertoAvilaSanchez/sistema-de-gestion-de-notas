from fastapi import APIRouter, HTTPException

from config.db import Session
from models.address import Address
from models.client import Client
from schemas.address import AddressSchema

address_router = APIRouter(prefix="/addresses", tags=["Address"])


@address_router.get("")
async def get_addresses():
    try:
        with Session() as session:
            addresses = session.query(Address).limit(10).all()
            if not addresses:
                raise HTTPException(status_code=404, detail="Addresses not found")
            return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@address_router.get("/{address_id}")
async def get_address(address_id: int):
    try:
        with Session() as session:
            address = (
                session.query(Address).filter(Address.address_id == address_id).first()
            )
            if not address:
                raise HTTPException(status_code=404, detail="Address not found")
            return address
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@address_router.get("/client/{client_id}")
async def get_address_by_client(client_id: int):
    try:
        with Session() as session:
            addresses = (
                session.query(Address).filter(Address.client_id == client_id).all()
            )
            if not addresses:
                raise HTTPException(status_code=404, detail="Address not found")
            return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@address_router.post("", response_model=AddressSchema)
async def create_address(address: AddressSchema):
    try:
        with Session() as session:
            client_exists = (
                session.query(Client)
                .filter(Client.client_id == address.client_id)
                .first()
            )
            if not client_exists:
                raise HTTPException(status_code=400, detail="Client not found")

            new_address = Address(
                client_id=address.client_id,
                neighborhood=address.neighborhood,
                address=address.address,
                address_number=address.address_number,
                reference=address.reference,
                ubication_url=address.ubication_url,
            )

            session.add(new_address)
            session.commit()
            session.refresh(new_address)
            return new_address

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@address_router.put("/{address_id}", response_model=AddressSchema)
async def update_address(address_id: int, address: AddressSchema):
    try:
        with Session() as session:
            address_exists = (
                session.query(Address).filter(Address.address_id == address_id).first()
            )
            if not address_exists:
                raise HTTPException(status_code=404, detail="Address not found")

            client_exists = (
                session.query(Client)
                .filter(Client.client_id == address.client_id)
                .first()
            )
            if not client_exists:
                raise HTTPException(status_code=400, detail="Client not found")

            address_exists.client_id = address.client_id
            address_exists.neighborhood = address.neighborhood
            address_exists.address = address.address
            address_exists.address_number = address.address_number
            address_exists.reference = address.reference
            address_exists.ubication_url = address.ubication_url

            session.commit()
            session.refresh(address_exists)
            return address_exists

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@address_router.delete("/{address_id}")
async def delete_address(address_id: int):
    try:
        with Session() as session:
            address = (
                session.query(Address).filter(Address.address_id == address_id).first()
            )
            if not address:
                raise HTTPException(status_code=404, detail="Address not found")
            session.delete(address)
            session.commit()
            return {"detail": "Address deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
