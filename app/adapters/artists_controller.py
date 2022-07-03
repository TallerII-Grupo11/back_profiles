import logging
from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.adapters.dtos.artists import (
    ArtistResponseDto,
    ArtistRequestDto,
    UpdateArtistRequestDto,
    CompleteArtistResponseDto,
)
from app.db import DatabaseManager, get_database
from app.db.impl.artist_manager import ArtistManager
from app.db.model.artist import ArtistModel, UpdateArtistModel
from app.db.model.artist import CompleteArtistModel
from app.rest import get_restclient_user, get_restclient_multimedia
from app.rest.users_client import UserClient
from app.rest.dtos.request.album import AlbumRequestDto
from app.rest.dtos.request.user import UserRequestDto, UpdateUserRequestDto
from app.rest.dtos.request.song import SongRequestDto
from app.rest.multimedia_client import MultimediaClient

router = APIRouter(tags=["artists"])


@router.post(
    "/artists",
    response_description="Add new artist profile",
    response_model=CompleteArtistResponseDto,
)
async def create_profile(
    req: ArtistRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_user: UserClient = Depends(get_restclient_user),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
):
    manager = ArtistManager(db.db)
    try:
        user_req = UserRequestDto(
            firebase_id=req.firebase_id,
            first_name=req.first_name,
            last_name=req.last_name,
            role="ARTIST",
            location=req.location,
            email=req.email,
        )
        user = rest_user.create_user(user_req)
        artist_model = ArtistModel(user_id=user.id, songs=req.songs, albums=req.albums)

        created_profile = await manager.add_profile(artist_model)

        albums = rest_media.get_albums(created_profile["albums"])
        songs = rest_media.get_songs(created_profile["songs"])

        complete_artist_model = CompleteArtistModel(
            user_id=user.id,
            albums=albums,
            songs=songs,
        )
        artist = ArtistModel(**created_profile)
        dto = CompleteArtistResponseDto.from_models(artist, user, complete_artist_model)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=jsonable_encoder(dto)
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Could not create User. Exception: {e}"
        )


@router.get(
    "/artists",
    response_description="Get a single artist profile",
    response_model=List[ArtistResponseDto],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    user_id: Optional[str] = None,
    db: DatabaseManager = Depends(get_database),
    rest_user: UserClient = Depends(get_restclient_user),
):
    manager = ArtistManager(db.db)
    profiles = await manager.get_all_profiles(user_id)

    user_ids = []
    for profile in profiles:
        user_ids.append(profile["user_id"])

    logging.info(f"user_ids -> {user_ids}")

    try:
        users = rest_user.all(','.join(user_ids))
        users_map = {}

        for user in users:
            users_map[user.id] = user

        artists = []
        for profile in profiles:
            artist_model = ArtistModel(**profile)
            user = users_map.get(artist_model.user_id)
            if user:
                artists.append(ArtistResponseDto.from_artist_model(artist_model, user))
            else:
                logging.error(f"User with id {artist_model.user_id} not found")

        return artists
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error getting Users info. Exception {e}"
        )


@router.get(
    "/artists/{artist_id}",
    response_description="Get a single artist profile",
    response_model=CompleteArtistResponseDto,
    status_code=status.HTTP_200_OK,
)
async def show_profile(
    artist_id: str,
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    manager = ArtistManager(db.db)
    profile = await manager.get_profile(id=artist_id)
    if profile is None:
        raise HTTPException(
            status_code=404, detail=f"Artist's Profile {artist_id} not found"
        )

    try:
        artist = ArtistModel(**profile)
        user = rest_user.get(artist.user_id)

        albums = rest_media.get_albums(profile["albums"])
        songs = rest_media.get_songs(profile["songs"])

        complete_artist_model = CompleteArtistModel(
            user_id=artist.user_id,
            albums=albums,
            songs=songs,
        )
        dto = CompleteArtistResponseDto.from_models(artist, user, complete_artist_model)
        return dto
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"User data not found. Exception {e}"
        )


@router.put(
    "/artists/{artist_id}",
    response_description="Update an artist's profile",
    response_model=CompleteArtistResponseDto,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    artist_id: str,
    req: UpdateArtistRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    manager = ArtistManager(db.db)
    try:
        # update profile
        artist = UpdateArtistModel(
            songs=req.songs,
            albums=req.albums,
        )
        response = await manager.update_profile(id=artist_id, profile=artist)
        if not response:
            raise HTTPException(status_code=404, detail=f"Artist {artist_id} not found")

        artist = ArtistModel(**response)
        # update user
        user_req = UpdateUserRequestDto(
            firebase_id=req.firebase_id,
            first_name=req.first_name,
            last_name=req.last_name,
            role="ARTIST",
            location=req.location,
            email=req.email,
            status=req.status,
        )
        user = rest_user.update(artist.user_id, user_req)

        albums = rest_media.get_albums(artist.albums)
        songs = rest_media.get_songs(artist.songs)

        complete_artist_model = CompleteArtistModel(
            user_id=artist.user_id,
            albums=albums,
            songs=songs,
        )
        dto = CompleteArtistResponseDto.from_models(artist, user, complete_artist_model)
        return dto
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error updating User. Exception {e}"
        )


@router.delete(
    "/artists/{artist_id}",
    response_description="Delete a profile artist",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(artist_id: str, db: DatabaseManager = Depends(get_database)):
    manager = ArtistManager(db.db)
    delete_result = await manager.delete_profile(artist_id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Artist {artist_id} not found")


# MULTIMEDIA
@router.post(
    "/artists/{artist_id}/albums",
    response_description="Create new album for artist",
    response_model=CompleteArtistResponseDto,
)
async def create_album(
    artist_id: str,
    album: AlbumRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    album, album_id = rest_media.create_album(album)
    manager = ArtistManager(db.db)
    artist = await manager.add_album(id=artist_id, album_id=album_id)
    user = rest_user.get(artist.user_id)
    albums = rest_media.get_albums(profile["albums"])
    songs = rest_media.get_songs(profile["songs"])

    complete_artist_model = CompleteArtistModel(
        user_id=artist.user_id,
        albums=albums,
        songs=songs,
    )
    dto = CompleteArtistResponseDto.from_models(
        artist, user, complete_artist_model, artist_id
    )
    return dto 
    #return JSONResponse(status_code=status.HTTP_201_CREATED, content=album)


@router.post(
    "/artists/{artist_id}/albums/{album_id}/songs",
    response_description="Create new song for artist and album",
    response_model=CompleteArtistResponseDto,
)
async def create_song(
    artist_id: str,
    album_id: str,
    song: SongRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    song, song_id = rest_media.create_song(song)
    if rest.add_song_to_album(album_id, song_id):
        manager = ArtistManager(db.db)
        artist = await manager.add_song(id=artist_id, song_id=song_id)
        user = rest_user.get(artist.user_id)

        albums = rest_media.get_albums(profile["albums"])
        songs = rest_media.get_songs(profile["songs"])

        complete_artist_model = CompleteArtistModel(
            user_id=artist.user_id,
            albums=albums,
            songs=songs,
        )
        dto = CompleteArtistResponseDto.from_models(
            artist, user, complete_artist_model, artist_id
        )
        return dto 
        #return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
    raise HTTPException(status_code=404, detail=f"Error add song in album {album_id}")
