import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Body

from app.db.model.listener import ListenerModel, UpdateListenerModel
from app.db.model.subscription import Subscription
from fastapi.encoders import jsonable_encoder


class ListenerManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_profile(self, user_id: str) -> ListenerModel:
        profile = await self.db["listeners"].find_one({"user_id": user_id})
        if profile:
            return ListenerModel(**profile)
        return profile

    async def add_profile(self, user_id: str):
        profile_model = ListenerModel(user_id=user_id, subscription=Subscription.free)
        profile = jsonable_encoder(profile_model)
        await self.db["listeners"].insert_one(profile)
        return profile

    async def update_profile(self, listener: UpdateListenerModel = Body(...)) -> bool:
        listener = {k: v for k, v in listener.dict().items() if v is not None}

        user_id = listener["user_id"]
        if listener["subscription"]:
            return await self.update_subcription(user_id=user_id,
                                                 subscription=listener["subscription"]
                                                 )
        if listener["follow_artist"]:
            return await self.follow_artist(user_id=user_id,
                                            artist_id=listener["follow_artist"]
                                            )
        if listener["favorite_song"]:
            return await self.add_favorite_song(user_id=user_id,
                                                song_id=listener["favorite_song"]
                                                )
        if listener["favorite_album"]:
            return await self.add_favorite_album(user_id=user_id,
                                                 album_id=listener["favorite_album"]
                                                 )
        if listener["favorite_playlist"]:
            return await self.add_favorite_playlist(user_id=user_id,
                                                    playlist_id=listener["favorite_playlist"]
                                                    )
        if listener["interest"]:
            return await self.add_interest(user_id=user_id,
                                           interest=listener["interest"]
                                           )
        if listener["my_playlist"]:
            return await self.create_playlist(user_id=user_id,
                                              playlist_id=listener["my_playlist"]
                                              )
        return False

    async def create_playlist(self, user_id: str, playlist_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"playlists": playlist_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[CREATE PLAYLIST] Fail with msg: {e}")
            return False

    async def update_subcription(self, user_id: str, subscription: str) -> bool:
        try:
            await self.db["listeners"]\
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
            await self.db["listeners"]\
                  .update_one({"user_id": user_id},
                              {"$$addToSet": {"follow_artists": artist_id}}
                              )
            return True
        except Exception as e:
            logging.error(f"[FOLLOW ARTIST] Fail with msg: {e}")
            return False

    async def add_favorite_song(self, user_id: str, song_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"favorite_songs": song_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE SONG] Fail with msg: {e}")
            return False

    async def add_favorite_album(self, user_id: str, album_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"favorite_albums": album_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE ALBUM] Fail with msg: {e}")
            return False

    async def add_favorite_playlist(self, user_id: str, playlist_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"favorite_playlists": playlist_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE PLAYLIST] Fail with msg: {e}")
            return False

    async def add_interest(self, user_id: str, interest: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"interests": interest}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD INTEREST] Fail with msg: {e}")
            return False
