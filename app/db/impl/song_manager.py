from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.profile import ProfileModel, UpdateProfileModel
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class ProfileManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_profile(self, user_id: str) -> SongModel:
        profile = await self.db["profiles"].find_one({"user_id": user_id})
        return ProfileModel(**profile)

    async def update_subcription(self, user_id: str, subscription: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one(
                            {"user_id": user_id}, 
                            {"$set": {"subscription": subscription}}
                            )
            return True
        except:
            return False

    async def add_profile(self, profile: ProfileModel = Body(...)):
        profile = jsonable_encoder(profile)
        await self.db["profiles"].insert_one(profile)
        return profile


    async def follow_artist(self, user_id: str, artist_id: str) -> bool:
        try:
            await self.db["profiles"]\
            .update_one({"user_id": user_id},
                        {"$push": {"follow_artists": artist_id}}
                        )
            return True
        except:
            return False

    async def favorite_song(self, user_id: str, song_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$push": {"favorite_songs": song_id}}
                            )
            return True
        except:
            return False

    async def favorite_album(self, user_id: str, album_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$push": {"favorite_albums": album_id}}
                            )
            return True
        except:
            return False

    async def favorite_playlist(self, user_id: str, playlist_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$push": {"favorite_playlists": playlist_id}}
                            )
            return True
        except:
            return False

    async def create_playlist(self, user_id: str, playlist_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$push": {"own_playlists": playlist_id}}
                            )
            return True
        except:
            return False




    """

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
                """
