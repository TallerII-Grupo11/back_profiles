from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.artist_manager import ArtistManager
from app.db.model.artist import ArtistModel

router = APIRouter(tags=["artists"])


@router.post(
    "/artists/{user_id}",
    response_description="Add new artist profile",
    response_model=ArtistModel
)
async def create_profile(
    user_id: str,
    db: DatabaseManager = Depends(get_database)
):
    manager = ArtistManager(db.db)
    created_profile = await manager.add_profile(user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)


@router.get(
    "/artists/{user_id}",
    response_description="Get a single artist profile",
    response_model=ArtistModel,
    status_code=status.HTTP_200_OK,
)
async def show_profile(user_id: str, db: DatabaseManager = Depends(get_database)):
    manager = ArtistManager(db.db)
    profile = await manager.get_profile(user_id=user_id)
    if profile is not None:
        return profile
    raise HTTPException(status_code=404, detail=f"Artist's Profile {user_id} not found")


@router.put(
    "/artists/{user_id}",
    response_description="Update a artist's profile",
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    user_id: str,
    song_id: str = None,
    album_id: str = None,
    db: DatabaseManager = Depends(get_database)
):
    manager = ArtistManager(db.db)
    msg = False
    if song_id:
        msg = await manager.add_song(user_id=user_id, song_id=song_id)
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error adding song"}
                                )
    if album_id:
        msg = await manager.add_album(user_id=user_id, album_id=album_id)
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error adding album"}
                                )
    if msg:
        return JSONResponse(
                            status_code=status.HTTP_201_CREATED,
                            content={"message": f"Success update of profile {user_id}"}
                            )

    raise HTTPException(status_code=404, detail=f"Artist's Profile {user_id} not found")
