from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    neighborhood = Column(String(50))
    address = Column(String(255))
    address_number = Column(String(50))
    reference = Column(String(255))
    ubication_url = Column(String(255))
    client = relationship("Client", back_populates="addresses")
