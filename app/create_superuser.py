from datetime import datetime
from getpass import getpass

from pymongo.collection import Collection
from pydantic import EmailStr

from db.database import user_collection
from models.user_services import create_user
from models.schemas import DBUser


def create_superuser(
    username: str,
    pwd: str,
    email: EmailStr,
    collection: Collection = user_collection
) -> None:
    """
    Create an admin user adn add it to the database.
    """
    data = {
        'disabled': False,
        'date_added': datetime.utcnow(),
        'is_admin': True,
    }
    # Update data with username and password
    data.update({'username': username})
    data.update({'password': pwd})
    data.update({'email': email})

    # Parse data into DBUser instance
    obj = DBUser.parse_obj(data)

    # Create user
    user = create_user(obj, collection)
    print(f"Superuser {user.username} created successfully!")


if __name__ == "__main__":
    username = input('Username: ')
    email = input('Email: ')
    pwd = getpass('Password: ')
    # Create superuser
    create_superuser(username, pwd, email)
