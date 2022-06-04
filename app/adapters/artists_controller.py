from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.artist_manager import ArtistManager
from app.db.model.artist import ArtistModel, UpdateArtistModel
from app.db.model.artist import CompleteArtistModel
from app.rest import get_restclient, get_restmultimedia
from app.rest.users_client import UserClient
from app.rest.dtos.album import AlbumRequestDto
from app.rest.dtos.song import SongRequestDto
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
    response_model=CompleteArtistModel,
    status_code=status.HTTP_200_OK,
)
async def show_profile(
    id: str,
    db: DatabaseManager = Depends(get_database),
    rest: MultimediaClient = Depends(get_restmultimedia),
):
    manager = ArtistManager(db.db)
    profile = await manager.get_profile(id=id)
    if profile is not None:
        albums = rest.get_albums(profile["albums"])
        profile["albums"] = albums

        songs = rest.get_songs(profile["songs"])
        profile["songs"] = songs

        return CompleteArtistModel(**profile)
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
    "/artists/{id}/albums",
    response_description="Create new album for artist",
    response_model=ArtistModel,
)
async def create_album(
    id: str,
    album: AlbumRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: MultimediaClient = Depends(get_restmultimedia),
):
    album, album_id = rest.create_album(album)
    manager = ArtistManager(db.db)
    response = await manager.add_album(id=id, album_id=album_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


@router.post(
    "/artists/{id}/albums/{album_id}/songs",
    response_description="Create new song for artist and album",
    response_model=ArtistModel,
)
async def create_song(
    id: str,
    album_id: str,
    song: SongRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: MultimediaClient = Depends(get_restmultimedia),
):
    song, song_id = rest.create_song(song)
    if rest.add_song_to_album(album_id, song_id):
        manager = ArtistManager(db.db)
        response = await manager.add_song(id=id, song_id=song_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
    raise HTTPException(status_code=404, detail=f"Error add song in album {album_id}")
