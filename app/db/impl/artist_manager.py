import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Body

from app.db.model.artist import ArtistModel, UpdateArtistModel
from fastapi.encoders import jsonable_encoder


class ArtistManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_profile(self, id: str) -> ArtistModel:
        profile = await self.db["artists"].find_one({"_id": id})
        if profile:
            return ArtistModel(**profile)
        return profile

    async def add_profile(self, artist: ArtistModel = Body(...)):
        profile = jsonable_encoder(artist)
        await self.db["artists"].insert_one(profile)
        return profile

    async def update_artist(
        self,
        id: str,
        artist: UpdateArtistModel = Body(...)
    ) -> bool:
        artist = {k: v for k, v in artist.dict().items() if v is not None}

        update = False
        profile = await self.db["artists"].find_one({"_id": id})
        if not profile:
            return False
        if "song" in artist:
            update = await self.add_song(id=id, song_id=artist["song"])
        if "album" in artist:
            update = await self.add_album(id=id, album_id=artist["album"])
        if "email" in artist:
            update = await self.update_email(id=id, email=artist["email"])
        return update

    async def add_song(self, id: str, song_id: str) -> bool:
        try:
            await self.db["artists"]\
                .update_one({"_id": id},
                            {"$addToSet": {"songs": song_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD SONG] Fail with msg: {e}")
            return False

    async def add_album(self, id: str, album_id: str) -> bool:
        try:
            await self.db["artists"]\
                .update_one({"_id": id},
                            {"$addToSet": {"albums": album_id}}
                            )
            return True
        except Exception as e:
            logging.error(f"[ADD ALBUM] Fail with msg: {e}")
            return False

    async def update_email(self, id: str, email: str) -> bool:
        try:
            await self.db["artists"]\
                .update_one({"_id": id},
                            {"$set": {"email": email}}
                            )
            return True
        except Exception as e:
            logging.error(f"[UPDATE MAIL] Fail with msg: {e}")
            return False
