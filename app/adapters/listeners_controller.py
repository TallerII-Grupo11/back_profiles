from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.rest import get_restmultimedia
from app.db.impl.listener_manager import ListenerManager
from app.db.model.listener import ListenerModel, UpdateListenerModel
from app.rest.dtos.playlist import PlaylistRequestDto, PlaylistSongResponseDto
from app.rest.multimedia_client import MultimediaClient
import logging
import json

router = APIRouter(tags=["listeners"])


@router.post(
    "/listeners",
    response_description="Add new listener profile",
    response_model=ListenerModel,
)
async def create_profile(
    listener: ListenerModel = Body(...), db: DatabaseManager = Depends(get_database)
):
    manager = ListenerManager(db.db)
    created_profile = await manager.add_profile(listener)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)


@router.get(
    "/listeners/{id}",
    response_description="Get a single listener profile",
    response_model=ListenerModel,
    status_code=status.HTTP_200_OK,
)
async def show_profile(id: str, db: DatabaseManager = Depends(get_database)):
    manager = ListenerManager(db.db)
    profile = await manager.get_profile(id=id)
    if profile is not None:
        return profile
    raise HTTPException(status_code=404, detail=f"Listener's Profile {id} not found")


@router.get(
    "/listeners",
    response_description="Get all listeners profiles",
    response_model=List[ListenerModel],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    user_id: Optional[str] = None, db: DatabaseManager = Depends(get_database)
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
):
    manager = ListenerManager(db.db)
    try:
        response = await manager.update_profile(id=id, profile=listener)
        if response:
            return response
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
    "/listeners/{user_id}/playlist",
    response_description="Create new playlist for listener",
    response_model=ListenerModel,
)
async def create_playlist(
    user_id: str,
    playlist: PlaylistRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: MultimediaClient = Depends(get_restmultimedia),
):
    playlist, playlist_id = rest.create_playlist(playlist)
    logging.info(f"[playlist] {playlist} - {playlist_id}")
    manager = ListenerManager(db.db)
    response = await manager.create_playlist(user_id=user_id, playlist_id=playlist_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

@router.get(
    "/listeners/{user_id}/playlists",
    response_description="Get all playlist of listener",
    response_model=List[PlaylistSongResponseDto],
)
async def get_playlists(
    user_id: str,
    db: DatabaseManager = Depends(get_database),
    rest: MultimediaClient = Depends(get_restmultimedia),
):
    manager = ListenerManager(db.db)
    user_profile = await manager.get_all_profiles(user_id=user_id)
    playlists = rest.get_playlists(user_profile["playlists"])
    return playlists
