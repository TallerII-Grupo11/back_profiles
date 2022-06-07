from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.adapters.dtos.listeners import (
    ListenerResponseDto,
    ListenerRequestDto,
    UpdateListenerRequestDto,
    CompleteListenerResponseDto,
)
from app.db import DatabaseManager, get_database
from app.rest import get_restclient_multimedia
from app.db.impl.listener_manager import ListenerManager
from app.db.model.listener import ListenerModel, UpdateListenerModel
from app.db.model.listener import CompleteListenerModel
from app.rest.dtos.request.playlist import PlaylistRequestDto
from app.rest.multimedia_client import MultimediaClient
import logging
from app.rest import UserClient, get_restclient_user
from app.rest.dtos.request.user import UserRequestDto, UpdateUserRequestDto

router = APIRouter(tags=["listeners"])


@router.post(
    "/listeners",
    response_description="Add new listener profile",
    response_model=ListenerResponseDto,
)
async def create_profile(
    req: ListenerRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: UserClient = Depends(get_restclient_user),
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
        user = rest.create_user(user_req)
        listener_model = ListenerModel(
            user_id=user.id,
            interests=req.interests,
        )

        created_profile = await manager.add_profile(listener_model)
        print(f"CREATED_PROFILE {created_profile}")
        print(f"CREATED_PROFILE_CONVERTED {ListenerModel(**created_profile)}")
        dto = ListenerResponseDto.from_listener_model(
            ListenerModel(**created_profile), user
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=jsonable_encoder(dto)
        )
    except Exception as e:
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
    rest_user: UserClient = Depends(get_restclient_user),
    rest_media: MultimediaClient = Depends(get_restclient_multimedia),
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
    user_id: Optional[str] = None, db: DatabaseManager = Depends(get_database)
):
    manager = ListenerManager(db.db)
    profiles = await manager.get_all_profiles(user_id)

    return profiles


@router.put(
    "/listeners/{listener_id}",
    response_description="Update a listener's profile",
    response_model=ListenerResponseDto,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    listener_id: str,
    req: UpdateListenerRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: UserClient = Depends(get_restclient_user),
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
        user = rest.update(listener.user_id, user_req)

        dto = ListenerResponseDto.from_listener_model(listener, user)
        return dto
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error updating User. Exception {e}"
        )


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
    rest: MultimediaClient = Depends(get_restclient_multimedia),
):
    playlist, playlist_id = rest.create_playlist(playlist)
    logging.info(f"[playlist] {playlist} - {playlist_id}")
    manager = ListenerManager(db.db)
    response = await manager.create_playlist(id=id, playlist_id=playlist_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
