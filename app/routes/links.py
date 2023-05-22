from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from pymongo.collection import Collection
from models.schemas import Link, LinkIn
from models.link_services import (
    get_links,
    get_link,
    add_link,
    check_that_link_exists
)
from db.database import collection
from bson import errors

router = APIRouter(
    prefix='/api/links',
    tags=['Links']
)


async def get_collection():
    """
    Return db collection.
    """
    yield collection


@router.get("/", response_model=list[Link], status_code=status.HTTP_200_OK)
async def links(db: Annotated[Collection, Depends(get_collection)]) -> list[Link] | list:
    """
    Get list of all available link objects form database.
    * All date data are returned in UTC time
    """
    return get_links(collection=db)


@router.get("/exists", response_model=None, status_code=status.HTTP_200_OK)
async def check_link_exist(url: str, db: Annotated[Collection, Depends(get_collection)]) -> dict:
    """
    Return boolean value that according to the link existence.
    """
    exists = check_that_link_exists(url, collection=db)
    if exists:
        return {'exists': check_that_link_exists(url, collection=db)}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Link already exists in the database"
    )


@router.get("/{item_id}", response_model=Link, status_code=status.HTTP_200_OK)
async def link(item_id: str, db: Annotated[Collection, Depends(get_collection)]):
    """
    Get a specific link based on given id.
    * All date data are returned in UTC time
    """
    try:
        return get_link(item_id, collection=db)
    except (ValueError, errors.InvalidId) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=Link, status_code=status.HTTP_201_CREATED)
async def add_new_link(data: LinkIn, db: Annotated[Collection, Depends(get_collection)]):
    """
    Add new link object to the database.
    Return added object.
    * All date data are returned in UTC time
    """
    try:
        return add_link(data, collection=db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
