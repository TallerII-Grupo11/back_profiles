from fastapi import APIRouter, status, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.song_manager import SongManager
from app.db.model.song import SongModel, UpdateSongModel
from typing import List

router = APIRouter(tags=["songs"])


@router.post(
    "/songs",
    response_description="Add new song",
    response_model=SongModel
)
async def create_song(
    song: SongModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = SongManager(db.db)
    created_song = await manager.add_song(song)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_song)


@router.get(
    "/songs",
    response_description="List all songs without album",
    include_in_schema=False,
    response_model=List[SongModel],
    status_code=status.HTTP_200_OK,
)
async def list_songs(db: DatabaseManager = Depends(get_database)):
    manager = SongManager(db.db)
    songs = await manager.list_songs_by_album()
    return songs


@router.get(
    "/songs/{id}",
    response_description="Get a single song",
    include_in_schema=False,
    response_model=SongModel,
    status_code=status.HTTP_200_OK,
)
async def show_song(id: str, db: DatabaseManager = Depends(get_database)):
    manager = SongManager(db.db)
    song = await manager.get_song(song_id=id)
    if song is not None:
        return song

    raise HTTPException(status_code=404, detail=f"Song {id} not found")


@router.put(
    "/songs/{id}",
    response_description="Update a song album",
    response_model=SongModel,
    status_code=status.HTTP_200_OK,
)
async def update_song(
    id: str,
    song: UpdateSongModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = SongManager(db.db)
    song = await manager.update_song(song_id=id, song=song)
    return song


@router.delete(
    "/songs/{id}",
    response_description="Delete a song",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def delete_song(id: str, db: DatabaseManager = Depends(get_database)):
    manager = SongManager(db.db)
    delete_result = await manager.delete_song(song_id=id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Song {id} not found")


@router.get(
    "/songs/",
    response_description="List all songs in by artist or album",
    response_model=List[SongModel],
    status_code=status.HTTP_200_OK,
)
async def list_songs_by(
    album_id: str = None,
    artist: str = None,
    db: DatabaseManager = Depends(get_database)
):
    manager = SongManager(db.db)
    if album_id:
        return await manager.list_songs_by_album(album_id)
    if artist:
        return await manager.list_songs_by_artist(artist)
    return await manager.list_songs_by_album()
