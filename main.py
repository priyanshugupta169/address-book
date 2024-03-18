from typing import List
from fastapi import FastAPI, HTTPException
from address_book.schemas import AddressCreate, AddressResponse, AddressUpdate, AddressSearch
from address_book.address_manager import AddressManager
from db import engine, Base

# Create tables in the database
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Routes
@app.post("/addresses/", response_model=AddressResponse)
def create_address(address: AddressCreate):
    """
    The function `create_address` adds a new address using the `AddressManager` class.
    
    :param address(AddressCreate): AddressCreate object that contains the details of the address to be created

    :return: The `create_address` function is returning the result of adding the address provided as a
    parameter to the `AddressManager` using the `add_address` method.
    """
    return AddressManager().add_address(address)

@app.get("/addresses/{address_id}", response_model=AddressResponse)
def read_address(address_id: int):
    """
    The `read_address` function retrieves an address from the database based on the provided address ID
    and raises a 404 error if the address is not found.
    
    :param address_id(int): The `address_id` parameter is an integer that represents the unique identifier of
    an address in the database. The `read_address` function takes this `address_id` as input, retrieves
    the address information from the database using `AddressManager().get_address_by_id(address_id)`,
    and returns the address

    :return: The function `read_address` is returning the address information retrieved from the
    database for the given `address_id`. If the address is not found in the database, it raises an
    HTTPException with a status code of 404 and the detail message "Address not found".
    """
    db_address = AddressManager().get_address_by_id(address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressUpdate):
    """
    This Python function updates an address in the database and raises a 404 error if the address is not
    found.
    
    :param address_id(int): The `address_id` parameter is an integer that represents the unique identifier of
    the address that needs to be updated in the database
    :param address(AddressUpdate): The `address` parameter in the `update_address` function is of type `AddressUpdate`.
    This likely represents a data structure or class that contains the updated information for an
    address, such as the street, city, state, and postal code. When calling the `update_address`
    function, you would

    :return: the updated address from the database.
    """
    db_address = AddressManager().update_address(address_id, address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return db_address

@app.delete("/addresses/{address_id}")
def delete_address(address_id: int):
    """
    The function `delete_address` deletes an address by its ID and returns a success message or raises a
    404 error if the address is not found.
    
    :param address_id(int): The `address_id` parameter is an integer that represents the unique identifier of
    the address that needs to be deleted from the system. This identifier is used to locate and remove
    the specific address record from the database or storage system

    :return: a dictionary with a message indicating that the address was deleted successfully.
    """
    deleted = AddressManager().delete_address(address_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}

# Route to retrieve addresses within a given distance from a specified location
@app.post("/addresses/within_distance/", response_model=List[AddressResponse])
def addresses_within_distance(address_search: AddressSearch):
    """
    This function takes an AddressSearch object and returns a list of addresses within a specified
    distance from the given latitude and longitude.
    
    :param address_search(AddressSearch): AddressSearch object containing latitude, longitude, and distance for
    searching nearby addresses

    :return: The function `addresses_within_distance` is returning a list of addresses that are within
    the specified distance from the provided latitude and longitude coordinates.
    """
    lat = address_search.latitude
    lon = address_search.longitude
    distance = address_search.distance
    addresses_within_distance = AddressManager().search_closest_address(lat, lon, distance)
    return addresses_within_distance
