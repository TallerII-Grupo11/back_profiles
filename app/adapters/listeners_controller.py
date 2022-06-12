from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.rest import get_restclient_user, get_restclient_multimedia
from app.db.impl.listener_manager import ListenerManager
from app.db.model.listener import ListenerModel, UpdateListenerModel
from app.db.model.listener import CompleteListenerResponseDto
from app.rest.dtos.request.playlist import PlaylistRequestDto
from app.rest.dtos.song import SongResponseDto
from app.rest.multimedia_client import MultimediaClient
import logging

router = APIRouter(tags=["listeners"])


@router.post(
    "/listeners",
    response_description="Add new listener profile",
    response_model=ListenerModel,
)
async def create_profile(
    listener: ListenerModel = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia)
):
    manager = ListenerManager(db.db)
    profile = await manager.add_profile(listener)
    if profile is not None:
        playlists = rest_media.get_playlists(profile["playlists"])
        profile["playlists"] = playlists
        created_profile = CompleteListenerModel(**profile)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)


@router.get(
    "/listeners/{id}",
    response_description="Get a single listener profile",
    response_model=CompleteListenerModel,
    status_code=status.HTTP_200_OK,
)
async def show_profile(
    id: str,
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    manager = ListenerManager(db.db)
    profile = await manager.get_profile(id=id)
    try:
        listener = ListenerModel(**profile)
        user = rest_user.get(listener.user_id)
        playlists = rest_media.get_playlists(listener.playlists)
        complete_listener_model = CompleteListenerModel(
            user_id=listener.user_id,
            playlists=playlists,
        )
        dto = CompleteListenerResponseDto.from_models(
            listener, user, complete_listener_model
        )
        return dto
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"User data not found. Exception {e}"
        )


@router.get(
    "/listeners",
    response_description="Get all listeners profiles",
    response_model=List[ListenerModel],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    user_id: Optional[str] = None,
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
):
    manager = ListenerManager(db.db)
    profiles = await manager.get_all_profiles(user_id)

    return profiles


@router.put(
    "/listeners/{id}",
    response_description="Update a listener's profile",
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    id: str,
    listener: UpdateListenerModel = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia)
):
    manager = ListenerManager(db.db)
    try:
        profile = await manager.update_profile(id=id, profile=listener)
        if profile is not None:
            playlists = rest_media.get_playlists(profile["playlists"])
            profile["playlists"] = playlists
            return CompleteListenerModel(**profile)
        raise HTTPException(status_code=404, detail=f"Listener {id} not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.delete(
    "/listeners/{id}",
    response_description="Delete a profile listener",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(id: str, db: DatabaseManager = Depends(get_database)):
    manager = ListenerManager(db.db)
    delete_result = await manager.delete_profile(id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Listener {id} not found")


# MULTIMEDIA
@router.post(
    "/listeners/{id}/playlists",
    response_description="Create new playlist for listener",
    response_model=ListenerModel,
)
async def create_playlist(
    id: str,
    playlist: PlaylistRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
):
    playlist, playlist_id = rest_media.create_playlist(playlist)
    logging.info(f"[playlist] {playlist} - {playlist_id}")
    manager = ListenerManager(db.db)
    response = await manager.create_playlist(id=id, playlist_id=playlist_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


# RECOMENDATION
@router.get(
    "/listeners/{id}/recomendations",
    response_description="Get recomendation of songs by listeners interest",
    response_model=List[SongResponseDto],
    status_code=status.HTTP_200_OK,
)
async def get_recomendations(
    id: str,
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
):
    manager = ListenerManager(db.db)
    profile = await manager.get_profile(id=id)
    songs = rest_media.get_recomendation_by_genre(profile["interests"])

    return songs
