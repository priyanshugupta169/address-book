from sqlalchemy import Column, Integer, String, ForeignKey, Float, CheckConstraint
from sqlalchemy.orm import relationship
from db import Base


# Model for the address
# This Python class represents an Address entity with attributes for street, city, state, postal code,
# latitude, and longitude.
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    state = Column(String(20), index=True, nullable=False)
    postal_code = Column(Integer, nullable=False, unique=True)
    latitude = Column(Float, index=True, nullable=False)
    longitude = Column(Float, index=True, nullable=False)

    # Check constraint to limit postal_code to 5 digits
    __table_args__ = (
        CheckConstraint('postal_code <= 999999', name='postal_code_max_value'),
    )
