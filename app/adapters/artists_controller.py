from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.artist_manager import ArtistManager
from app.db.model.artist import ArtistModel, UpdateArtistModel
from app.rest import get_restclient, get_restmultimedia
from app.rest.users_client import UserClient
from app.rest.dtos.song import SongResponseDto, SongRequestDto
from app.rest.dtos.album import AlbumResponseDto, AlbumRequestDto
from app.rest.multimedia_client import MultimediaClient

router = APIRouter(tags=["artists"])


@router.post(
    "/artists",
    response_description="Add new artist profile",
    response_model=ArtistModel,
)
async def create_profile(
    artist: ArtistModel = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: UserClient = Depends(get_restclient),
):
    manager = ArtistManager(db.db)
    created_profile = await manager.add_profile(artist)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)


@router.get(
    "/artists",
    response_description="Get a single artist profile",
    response_model=List[ArtistModel],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    user_id: Optional[str] = None,
    db: DatabaseManager = Depends(get_database),
    rest: UserClient = Depends(get_restclient),
):
    # test
    user = rest.get()
    print(user.firebase_id)
    print(user.email)
    manager = ArtistManager(db.db)
    profiles = await manager.get_all_profiles(user_id)

    return profiles


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
    db: DatabaseManager = Depends(get_database),
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


# MULTIMEDIA
@router.post(
    "/artists/{user_id}/album",
    response_description="Create new album for artist",
    response_model=ArtistModel,
)
async def create_album(
    user_id: str,
    album: AlbumRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: MultimediaClient = Depends(get_restmultimedia),
):
    album = rest.create_album(album)
    manager = ArtistManager(db.db)
    response = manager.add_album(user_id=user_id, album_id=album["_id"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
