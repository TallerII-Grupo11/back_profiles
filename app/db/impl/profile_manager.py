from typing import List
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.profile import ProfileModel, UpdateProfileModel
from app.db.model.subscription import Subscription
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class ProfileManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_profile(self, user_id: str) -> ProfileModel:
        profile = await self.db["profiles"].find_one({"user_id": user_id})
        if profile:
            return ProfileModel(**profile)
        return profile

    async def add_profile(self, user_id: str):
        profile_model = ProfileModel(user_id=user_id, subscription=Subscription.free)
        profile = jsonable_encoder(profile_model)
        await self.db["profiles"].insert_one(profile)
        return profile

    async def create_playlist(self, user_id: str, playlist_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"playlists": playlist_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[CREATE PLAYLIST] Fail with msg: {e}")
            return False


    async def update_subcription(self, user_id: str, subscription: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one(
                            {"user_id": user_id}, 
                            {"$set": {"subscription": subscription}}
                            )
            return True
        except Exception as e:
            logging.error(f"[CHANGE SUBSCRIPTION] Fail with msg: {e}")
            return False

    async def follow_artist(self, user_id: str, artist_id: str) -> bool:
        try:
            await self.db["profiles"]\
            .update_one({"user_id": user_id},
                        {"$$addToSet": {"follow_artists": artist_id}}
                        )
            return True
        except Exception as e:
            logging.error(f"[FOLLOW ARTIST] Fail with msg: {e}")
            return False

    async def add_favorite_song(self, user_id: str, song_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"favorite_songs": song_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE SONG] Fail with msg: {e}")
            return False

    async def add_favorite_album(self, user_id: str, album_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"favorite_albums": album_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE ALBUM] Fail with msg: {e}")
            return False

    async def add_favorite_playlist(self, user_id: str, playlist_id: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"favorite_playlists": playlist_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE PLAYLIST] Fail with msg: {e}")
            return False

    async def add_interest(self, user_id: str, interest: str) -> bool:
        try:
            await self.db["profiles"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"interests": interest}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD INTEREST] Fail with msg: {e}")
            return False
