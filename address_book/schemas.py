from pydantic import BaseModel, conint
from typing import Optional


# Pydantic model for creating an address
class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: conint(ge=100000, le=999999)
    latitude: float
    longitude: float

# Pydantic model for updating an address
class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[conint(ge=100000, le=999999)] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# Pydantic model for address response
class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    state: str
    postal_code: conint(ge=100000, le=999999)
    latitude: float
    longitude: float

# Pydantic model for query parameters
class AddressSearch(BaseModel):
    latitude: float
    longitude: float
    distance: float
