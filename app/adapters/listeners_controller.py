from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import traceback

from app.adapters.dtos.listeners import (
    ListenerResponseDto,
    UpdateListenerRequestDto,
    ListenerRequestDto,
    CompleteListenerResponseDto,
)
from app.db import DatabaseManager, get_database
from app.rest import get_restclient_user, get_restclient_multimedia
from app.db.impl.listener_manager import ListenerManager
from app.db.model.listener import (
    ListenerModel,
    UpdateListenerModel,
    CompleteListenerModel,
)
from app.rest.dtos.request.playlist import PlaylistRequestDto
from app.rest.dtos.request.user import UpdateUserRequestDto, UserRequestDto
from app.rest.dtos.song import SongResponseDto
from app.rest.multimedia_client import MultimediaClient
from app.rest.users_client import UserClient

import logging

router = APIRouter(tags=["listeners"])


@router.post(
    "/listeners",
    response_description="Add new listener profile",
    response_model=CompleteListenerResponseDto,
)
async def create_profile(
    req: ListenerRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_user: UserClient = Depends(get_restclient_user),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
):
    manager = ListenerManager(db.db)
    try:
        user_req = UserRequestDto(
            firebase_id=req.firebase_id,
            first_name=req.first_name,
            last_name=req.last_name,
            role="LISTENER",
            location=req.location,
            email=req.email,
        )
        user = rest_user.create_user(user_req)
        listener_model = ListenerModel(
            user_id=user.id,
            subscription=req.subscription,
            interests=req.interests,
            playlists=req.playlists,
        )

        created_profile = await manager.add_profile(listener_model)
        listener = ListenerModel(**created_profile)

        playlists = rest_media.get_playlists(listener.playlists)
        complete_listener_model = CompleteListenerModel(
            user_id=listener.user_id,
            playlists=playlists,
        )

        dto = CompleteListenerResponseDto.from_models(
            listener, user, complete_listener_model
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=jsonable_encoder(dto)
        )
    except Exception as e:
        print(traceback.print_exc())
        raise HTTPException(
            status_code=400, detail=f"Could not create User. Exception: {e}"
        )


@router.get(
    "/listeners/{listener_id}",
    response_description="Get a single listener profile",
    response_model=CompleteListenerResponseDto,
    status_code=status.HTTP_200_OK,
)
async def show_profile(
    listener_id: str,
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    manager = ListenerManager(db.db)
    profile = await manager.get_profile(id=listener_id)
    if profile is None:
        raise HTTPException(
            status_code=404, detail=f"Listener's Profile {listener_id} not found"
        )

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
    response_model=List[CompleteListenerResponseDto],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    user_id: Optional[str] = None,
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    manager = ListenerManager(db.db)
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

        listeners = []
        for profile in profiles:
            listener_model = ListenerModel(**profile)
            user = users_map.get(profile["user_id"])

            playlists = rest_media.get_playlists(profile["playlists"])
            complete_listener_model = CompleteListenerModel(
                user_id=profile["user_id"],
                playlists=playlists,
            )
            if user:
                listeners.append(
                    CompleteListenerResponseDto.from_models(
                        listener_model, user, complete_listener_model
                    )
                )
            else:
                logging.error(f"User with id {profile['user_id']} not found")

        return listeners
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error getting Users info. Exception {e}"
        )


@router.put(
    "/listeners/{listener_id}",
    response_description="Update a listener's profile",
    response_model=CompleteListenerResponseDto,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    listener_id: str,
    req: UpdateListenerRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_user: UserClient = Depends(get_restclient_user),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
):
    manager = ListenerManager(db.db)
    try:
        # update profile
        listener = UpdateListenerModel(
            interests=req.interests,
        )
        response = await manager.update_profile(id=listener_id, profile=listener)
        if not response:
            raise HTTPException(
                status_code=404, detail=f"Listener {listener_id} not found"
            )

        listener = ListenerModel(**response)
        # update user
        user_req = UpdateUserRequestDto(
            firebase_id=req.firebase_id,
            first_name=req.first_name,
            last_name=req.last_name,
            role="LISTENER",
            location=req.location,
            email=req.email,
            status=req.status,
        )
        user = rest_user.update(listener.user_id, user_req)
        playlists = rest_media.get_playlists(listener.playlists)

        complete_listener_model = CompleteListenerModel(
            user_id=listener.user_id,
            playlists=playlists,
        )

        dto = CompleteListenerResponseDto.from_models(
            listener, user, complete_listener_model
        )
        return dto
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error updating User. Exception {e}"
        )


@router.delete(
    "/listeners/{listener_id}",
    response_description="Delete a profile listener",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(listener_id: str, db: DatabaseManager = Depends(get_database)):
    manager = ListenerManager(db.db)
    delete_result = await manager.delete_profile(listener_id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Listener {listener_id} not found")


# MULTIMEDIA
@router.post(
    "/listeners/{listener_id}/playlists",
    response_description="Create new playlist for listener",
    response_model=CompleteListenerResponseDto,
)
async def create_playlist(
    listener_id: str,
    playlist: PlaylistRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
    rest_user: UserClient = Depends(get_restclient_user),
):
    playlist, playlist_id = rest_media.create_playlist(playlist)
    manager = ListenerManager(db.db)

    listener = await manager.create_playlist(id=listener_id, playlist_id=playlist_id)
    user = rest_user.get(listener.user_id)
    playlists = rest_media.get_playlists(listener["playlists"])
    complete_listener_model = CompleteListenerModel(
        user_id=listener.user_id,
        playlists=playlists,
    )
    dto = CompleteListenerResponseDto.from_models(
        listener, user, complete_listener_model, listener_id
    )
    # return dto
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=dto)


# RECOMMENDATION
@router.get(
    "/listeners/{listener_id}/recommendations",
    response_description="Get recommendation of songs by listeners interest",
    response_model=List[SongResponseDto],
    status_code=status.HTTP_200_OK,
)
async def get_recommendations(
    listener_id: str,
    db: DatabaseManager = Depends(get_database),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
):
    try:
        manager = ListenerManager(db.db)
        profile = await manager.get_profile(id=listener_id)
        songs = rest_media.get_recomendation_by_genre(profile["interests"])

        return songs
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Listener {listener_id} not found. Error: {e}"
        )
