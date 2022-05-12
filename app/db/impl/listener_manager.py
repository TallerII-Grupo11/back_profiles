import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Body

from app.db.model.listener import ListenerModel, UpdateListenerModel
from fastapi.encoders import jsonable_encoder


class ListenerManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_profile(self, id: str) -> ListenerModel:
        profile = await self.db["listeners"].find_one({"_id": id})
        if profile:
            return ListenerModel(**profile)
        return profile

    async def add_profile(self, listener: ListenerModel = Body(...)):
        profile = jsonable_encoder(listener)
        await self.db["listeners"].insert_one(profile)
        return profile

    async def update_profile(
        self, id: str,
        listener: UpdateListenerModel = Body(...)
    ) -> bool:
        logging.info(f"[LISTENER] {listener}")
        listener = {k: v for k, v in listener.dict().items() if v is not None}

        update = False
        profile = await self.db["listeners"].find_one({"_id": id})
        if not profile:
            return False
        if "subscription" in listener:
            sub = listener["subscription"]
            update = await self.update_subcription(id=id,
                                                   subscription=sub
                                                   )
        if "follow_artist" in listener:
            update = await self.follow_artist(id=id,
                                              artist_id=listener["follow_artist"]
                                              )
        if "favorite_song" in listener:
            update = await self.add_favorite_song(id=id,
                                                  song_id=listener["favorite_song"]
                                                  )
        if "favorite_album" in listener:
            return await self.add_favorite_album(id=id,
                                                 album_id=listener["favorite_album"]
                                                 )
        if "favorite_playlist" in listener:
            play = listener["favorite_playlist"]
            update = await self.add_favorite_playlist(id=id,
                                                      playlist_id=play
                                                      )
        if "interest" in listener:
            update = await self.add_interest(id=id,
                                             interest=listener["interest"]
                                             )
        if "my_playlist" in listener:
            update = await self.create_playlist(id=id,
                                                playlist_id=listener["my_playlist"]
                                                )
        return update

    async def create_playlist(self, id: str, playlist_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"_id": id},
                            {"$addToSet": {"playlists": playlist_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[CREATE PLAYLIST] Fail with msg: {e}")
            return False

    async def update_subcription(self, id: str, subscription: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"_id": id},
                            {"$set": {"subscription": subscription}}
                            )
            return True
        except Exception as e:
            logging.error(f"[CHANGE SUBSCRIPTION] Fail with msg: {e}")
            return False

    async def follow_artist(self, id: str, artist_id: str) -> bool:
        try:
            await self.db["listeners"]\
                  .update_one({"_id": id},
                              {"$$addToSet": {"follow_artists": artist_id}}
                              )
            return True
        except Exception as e:
            logging.error(f"[FOLLOW ARTIST] Fail with msg: {e}")
            return False

    async def add_favorite_song(self, id: str, song_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"_id": id},
                            {"$addToSet": {"favorite_songs": song_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE SONG] Fail with msg: {e}")
            return False

    async def add_favorite_album(self, id: str, album_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"_id": id},
                            {"$addToSet": {"favorite_albums": album_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE ALBUM] Fail with msg: {e}")
            return False

    async def add_favorite_playlist(self, id: str, playlist_id: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"_id": id},
                            {"$addToSet": {"favorite_playlists": playlist_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD FAVORITE PLAYLIST] Fail with msg: {e}")
            return False

    async def add_interest(self, id: str, interest: str) -> bool:
        try:
            await self.db["listeners"]\
                .update_one({"_id": id},
                            {"$addToSet": {"interests": interest}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD INTEREST] Fail with msg: {e}")
            return False
