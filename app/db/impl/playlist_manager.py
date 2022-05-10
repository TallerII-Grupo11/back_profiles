from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.playlist import PlaylistModel, UpdatePlaylistModel, PlaylistSongModel
from app.db.impl.song_manager import SongManager
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class PlaylistManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.song_manager = SongManager(self.db)

    async def with_songs(self, playlist: PlaylistModel):
        songs_list = []
        for song_id in playlist["songs"]:
            song = await self.song_manager.get_song(song_id)
            songs_list.append(song)

        playlist_w_song = {"songs": songs_list,
                           "title": playlist["title"],
                           "description": playlist["description"],
                           "is_collaborative": playlist["is_collaborative"],
                           "user_owner": playlist["user_owner"]
                          }
        return PlaylistSongModel.parse_obj(playlist_w_song)

    async def get_playlists(self, user_id: str = None) -> List[PlaylistSongModel]:
        playlist_list = []
        if not user_id:
            playlist_q = self.db["playlists"].find()
        else:
            playlist_q = self.db["playlists"].find({"user_owner": user_id})

        async for playlist in playlist_q:
            playlist_list.append(PlaylistModel(**playlist))
        return playlist_list

    async def get_playlist(self, playlist_id: str) -> PlaylistSongModel:
        playlist = await self.db["playlists"].find_one({"_id": playlist_id})
        playlist_w_song = await self.with_songs(playlist)

        return playlist_w_song

    async def delete_playlist(self, playlist_id: str):
        delete_result = await self.db["playlists"].delete_one({"_id": playlist_id})
        return delete_result

    async def update_playlist(
        self,
        playlist_id: str,
        playlist: UpdatePlaylistModel = Body(...)
    ):
        playlist = {k: v for k, v in playlist.dict().items() if v is not None}
        playlist_to_update = await self.get_playlist(playlist_id)
        playlist_to_update = jsonable_encoder(playlist_to_update)

        if not (playlist["user_owner"] == playlist_to_update["user_owner"] or
                playlist_to_update["is_collaborative"] == "yes"):
            raise RuntimeError(f"User {playlist['user_owner']} \
                cant not edit Playlist {playlist_id}")

        if len(playlist) >= 1:
            if "songs" in playlist:
                list_songs = playlist["songs"]
                for song in list_songs:
                    await self.db["playlists"].update_one(
                        {"_id": playlist_id},
                        {"$push": {"songs": {"$each": playlist["songs"]}}}
                        )

                del playlist["songs"]
            await self.db["playlists"].update_one(
                                                    {"_id": playlist_id},
                                                    {"$set": playlist}
                                                 )

    async def add_playlist(self, playlist: PlaylistModel = Body(...)):
        playlist = jsonable_encoder(playlist)
        await self.db["playlists"].insert_one(playlist)
        return playlist
