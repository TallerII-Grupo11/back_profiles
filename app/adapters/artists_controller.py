from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.adapters.dtos.artists import ArtistResponseDto, ArtistRequestDto, UpdateArtistRequestDto
from app.db import DatabaseManager, get_database
from app.db.impl.artist_manager import ArtistManager
from app.db.model.artist import ArtistModel, UpdateArtistModel
from app.rest import get_restclient
from app.rest.dtos.request.user import UserRequestDto, UpdateUserRequestDto
from app.rest.users import UserClient

router = APIRouter(tags=["artists"])


@router.post(
    "/artists",
    response_description="Add new artist profile",
    response_model=ArtistResponseDto,
)
async def create_profile(
    req: ArtistRequestDto = Body(...),
    db: DatabaseManager = Depends(get_database),
    rest: UserClient = Depends(get_restclient),
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
        user = rest.create_user(user_req)
        artist_model = ArtistModel(
            user_id=user.id,
            songs=req.songs,
            albums=req.albums
        )

        created_profile = await manager.add_profile(artist_model)
        print(f"CREATED_PROFILE {created_profile}")
        print(f"CREATED_PROFILE_CONVERTED {ArtistModel(**created_profile)}")
        dto = ArtistResponseDto.from_artist_model(ArtistModel(**created_profile), user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(dto))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not create User. Exception: {e}")


@router.get(
    "/artists",
    response_description="Get a single artist profile",
    response_model=List[ArtistModel],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    user_id: Optional[str] = None,
    db: DatabaseManager = Depends(get_database),
):
    manager = ArtistManager(db.db)
    profiles = await manager.get_all_profiles(user_id)

    return profiles


@router.get(
    "/artists/{artist_id}",
    response_description="Get a single artist profile",
    response_model=ArtistResponseDto,
    status_code=status.HTTP_200_OK,
)
async def show_profile(
        artist_id: str,
        db: DatabaseManager = Depends(get_database),
        rest: UserClient = Depends(get_restclient),
):
    manager = ArtistManager(db.db)
    profile = await manager.get_profile(id=artist_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"Artist's Profile {artist_id} not found")

    try:
        artist = ArtistModel(**profile)
        user = rest.get(artist.user_id)
        dto = ArtistResponseDto.from_artist_model(artist, user)
        return dto
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User data not found. Exception {e}")


@router.put(
    "/artists/{artist_id}",
    response_description="Update an artist's profile",
    response_model=ArtistResponseDto,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
        artist_id: str,
        req: UpdateArtistRequestDto = Body(...),
        db: DatabaseManager = Depends(get_database),
        rest: UserClient = Depends(get_restclient),
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
        user = rest.update(artist.user_id, user_req)

        dto = ArtistResponseDto.from_artist_model(artist, user)
        return dto
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating User. Exception {e}")


@router.delete(
    "/artists/{artist_id}",
    response_description="Delete a profile artist",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(
        artist_id: str,
        db: DatabaseManager = Depends(get_database)
):
    manager = ArtistManager(db.db)
    delete_result = await manager.delete_profile(artist_id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Artist {artist_id} not found")
