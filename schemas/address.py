from typing import Optional

from pydantic import BaseModel


class AddressSchema(BaseModel):
    address_id: Optional[int]
    client_id: int
    neighborhood: str
    address: str
    address_number: str
    reference: str
    ubication_url: str
