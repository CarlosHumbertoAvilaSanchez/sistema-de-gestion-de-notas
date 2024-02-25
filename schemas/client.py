from typing import Optional

from pydantic import BaseModel


class ClientSchema(BaseModel):
    client_id: Optional[int]
    first_name: str
    last_name: str
    phone: str
