from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.artist_manager import ArtistManager
from app.db.model.artist import ArtistModel, UpdateArtistModel

router = APIRouter(tags=["artists"])


@router.post(
    "/artists",
    response_description="Add new artist profile",
    response_model=ArtistModel
)
async def create_profile(
    artist: ArtistModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = ArtistManager(db.db)
    created_profile = await manager.add_profile(artist)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)


@router.get(
    "/artists/{id}",
    response_description="Get a single artist profile",
    response_model=ArtistModel,
    status_code=status.HTTP_200_OK,
)
async def show_profile(id: str, db: DatabaseManager = Depends(get_database)):
    manager = ArtistManager(db.db)
    profile = await manager.get_profile(id=id)
    if profile is not None:
        return profile
    raise HTTPException(status_code=404, detail=f"Artist's Profile {id} not found")


@router.put(
    "/artists/{id}",
    response_description="Update a artist's profile",
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    id: str,
    artist: UpdateArtistModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = ArtistManager(db.db)
    try:
        response = await manager.update_profile(id=id, profile=artist)
        if response:
            return response
        raise HTTPException(status_code=404, detail=f"Artist {id} not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.delete(
    "/artists/{id}",
    response_description="Delete a profile artist",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(id: str, db: DatabaseManager = Depends(get_database)):
    manager = ArtistManager(db.db)
    delete_result = await manager.delete_profile(id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Artist {id} not found")