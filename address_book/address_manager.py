
from address_book.models import Address
from address_book.schemas import AddressCreate, AddressUpdate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import get_db

class AddressManager:

    def add_address(self, address: AddressCreate):
        """
        The function `add_address` adds a new address to the database while handling integrity errors
        and other exceptions.
        
        :param address(AddressCreate): AddressCreate model is used to create a new address entry in the database. It
        contains attributes such as street, city, state, and postal code. The `add_address`
        method takes an instance of AddressCreate as a parameter and adds a new address to the database
        using the provided information.

        :return: The function `add_address` is returning the `db_address` object after it has been
        successfully added to the database, committed, and refreshed.
        """
        db = get_db()
        try:
            db_address = Address(**address.model_dump())
            print(address)
            db.add(db_address)
            db.commit()
            db.refresh(db_address)
        except IntegrityError as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()
        return db_address
    
    def get_address_by_id(self, address_id: int):
        """
        This function retrieves an address from the database based on the provided address ID.
        
        :param address_id(int): The `get_address_by_id` function takes an `address_id` parameter of type
        integer. This parameter is used to query the database for an address with the matching ID and
        return the address information

        :return: The function `get_address_by_id` is returning the address object from the database that
        matches the provided `address_id`.
        """
        db = get_db()
        db_address = db.query(Address).filter(Address.id == address_id).first()
        db.close()
        return db_address
    
    def update_address(self, address_id: int, address: AddressUpdate):
        """
        This Python function updates an address in the database based on the provided address ID and
        AddressUpdate object.
        
        :param address_id(int): The `address_id` parameter in the `update_address` method is an integer that
        represents the unique identifier of the address that needs to be updated in the database. This
        identifier is used to locate the specific address record in the database that requires
        modification
        :param address(AddressUpdate): The `update_address` function you provided is used to update an existing address
        in the database. The function takes in two parameters:

        :return: The `update_address` function returns the updated `db_address` object after updating
        the address details in the database. If the `db_address` is `None` (not found in the database),
        it will return `None`.
        """
        db = get_db()
        try:
            db_address = db.query(Address).filter(Address.id == address_id).first()
            if db_address == None:
                return db_address
            for key, value in address.dict(exclude_unset=True).items():
                setattr(db_address, key, value)
            db.commit()
            db.refresh(db_address)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()
        return db_address

    def delete_address(self, address_id: int):
        """
        The function `delete_address` deletes an address from the database based on the provided address
        ID.
        
        :param address_id(int): The `address_id` parameter in the `delete_address` method is an integer that
        represents the unique identifier of the address that needs to be deleted from the database

        :return: The `delete_address` method returns a boolean value - `True` if the address with the
        specified `address_id` was successfully deleted from the database, and `False` if the address
        was not found in the database.
        """
        db = get_db()
        db_address = self.get_address_by_id(address_id)
        if db_address:
            db.delete(db_address)
            db.commit()
            db.close()
            return True
        return False
    
    def search_closest_address(self, lat: float, lon: float, distance: float):
        """
        The function `search_closest_address` retrieves addresses within a specified distance from a
        given latitude and longitude using Euclidean distance calculation.
        
        :param lat(float): Latitude of the target location to search for nearby addresses
        :param lon(float): Longitude is a geographic coordinate that specifies the east-west position of a
        point on the Earth's surface. It is measured in degrees, with values ranging from -180 to 180
        :param distance(float): The `distance` parameter in the `search_closest_address` function represents
        the maximum distance within which you want to search for addresses. The function will return a
        list of addresses that are within this specified distance from the given latitude and longitude
        coordinates

        :return: returns a list of addresses that are within a specified distance from a given latitude and longitude. 
        The addresses are retrieved from the database based on the Euclidean distance calculation 
        using the provided latitude, longitude, and distance parameters.
        """
        db = get_db()

        # pow and sqrt were not working somehow in sqlite+sqlalchemy
        # using euclidien distance
        addresses_within_distance = db.query(Address). \
            filter(
                (
                    (Address.latitude - lat)*(Address.latitude - lat) + 
                    (Address.longitude - lon)*(Address.longitude - lon)
                ) <= distance*distance
            ).all()
        db.close()
        return addresses_within_distance