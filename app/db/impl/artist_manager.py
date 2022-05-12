import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Body

from app.db.model.artist import ArtistModel, UpdateArtistModel
from fastapi.encoders import jsonable_encoder


class ArtistManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_profile(self, user_id: str) -> ArtistModel:
        profile = await self.db["artists"].find_one({"user_id": user_id})
        if profile:
            return ArtistModel(**profile)
        return profile

    async def add_profile(self, user_id: str):
        profile_model = ArtistModel(user_id=user_id)
        profile = jsonable_encoder(profile_model)
        await self.db["artists"].insert_one(profile)
        return profile

    async def update_artist(self,
                            artist: UpdateArtistModel = Body(...)
    ): -> bool
        artist = {k: v for k, v in artist.dict().items() if v is not None}

        if artist["song"]:
            return await self.add_song(user_id=artist["user_id"], song_id=artist["song"])
        if artist["album"]:
            return await self.add_album(user_id=artist["user_id"], album_id=artist["album"])
        if artist["email"]:
            return await self.update_email(user_id=artist["user_id"], email=artist["email"])
        return False

    async def add_song(self, user_id: str, song_id: str) -> bool:
        try:
            await self.db["artists"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"songs": song_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD SONG] Fail with msg: {e}")
            return False

    async def add_album(self, user_id: str, album_id: str) -> bool:
        try:
            await self.db["artists"]\
                .update_one({"user_id": user_id},
                            {"$addToSet": {"albums": album_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD ALBUM] Fail with msg: {e}")
            return False

    async def update_email(self, user_id: str, email: str) -> bool:
        try:
            await self.db["artists"]\
                .update_one({"user_id": user_id},
                            {"$set": {"email": email}}
                            )
            return True
        except Exception as e:
            logging.error(f"[UPDATE MAIL] Fail with msg: {e}")
            return False
