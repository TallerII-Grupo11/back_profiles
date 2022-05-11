from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.listener_manager import ListenerManager
from app.db.model.listener import ListenerModel

router = APIRouter(tags=["listeners"])


@router.post(
    "/listeners/{user_id}",
    response_description="Add new listener profile",
    response_model=ListenerModel
)
async def create_profile(
    user_id: str,
    db: DatabaseManager = Depends(get_database)
):
    manager = ListenerManager(db.db)
    created_profile = await manager.add_profile(user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)


@router.get(
    "/listeners/{user_id}",
    response_description="Get a single listener profile",
    response_model=ListenerModel,
    status_code=status.HTTP_200_OK,
)
async def show_profile(user_id: str, db: DatabaseManager = Depends(get_database)):
    manager = ListenerManager(db.db)
    profile = await manager.get_profile(user_id=user_id)
    if profile is not None:
        return profile
    raise HTTPException(status_code=404, detail=f"Listener's Profile {user_id} not found")


@router.put(
    "/listeners/{user_id}",
    response_description="Update a listener's profile",
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    user_id: str,
    subscription: str = None,
    artist_id: str = None,
    song_id: str = None,
    album_id: str = None,
    playlist_id: str = None,
    interest: str = None,
    db: DatabaseManager = Depends(get_database)
):
    manager = ListenerManager(db.db)
    msg = False
    if subscription:
        msg = await manager.update_subcription(user_id=user_id,
                                               subscription=subscription
                                               )
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error updating subscription"}
                                )
    if artist_id:
        msg = await manager.follow_artist(user_id=user_id, artist_id=artist_id)
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error follow artist"}
                                )
    if song_id:
        msg = await manager.add_favorite_song(user_id=user_id, song_id=song_id)
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error adding fav song"}
                                )
    if album_id:
        msg = await manager.add_favorite_album(user_id=user_id, album_id=album_id)
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error adding fav album"}
                                )
    if playlist_id:
        msg = await manager.add_favorite_playlist(user_id=user_id,
                                                  playlist_id=playlist_id
                                                  )
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error adding fav playlist"}
                                )
    if interest:
        msg = await manager.add_interest(user_id=user_id,
                                         interest=interest
                                         )
        if not msg:
            return JSONResponse(status_code=404,
                                content={"message": "Error adding interest"}
                                )
    if msg:
        return JSONResponse(
                            status_code=status.HTTP_201_CREATED,
                            content={"message": f"Success update of profile {user_id}"}
                            )

    raise HTTPException(status_code=404, detail=f"Listener's Profile {user_id} not found")


@router.put(
    "/listeners/{user_id}/playlist/{playlist_id}",
    response_description="Create playlist for listener",
    status_code=status.HTTP_200_OK,
)
async def update_playlist(
    user_id: str,
    playlist_id: str,
    db: DatabaseManager = Depends(get_database)
):
    manager = ListenerManager(db.db)
    playlist = await manager.create_playlist(user_id=user_id, playlist_id=playlist_id)
    if playlist:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Success add playlist"}
                            )
    raise JSONResponse(status_code=404,
                       content={"message": f"Listener's Profile {user_id} not found"})
