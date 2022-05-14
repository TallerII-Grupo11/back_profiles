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

    async def delete_profile(self, id: str):
        delete_result = await self.db["artists"].delete_one({"_id": id})
        return delete_result

    async def update_profile(
        self,
        id: str,
        profile: UpdateArtistModel = Body(...)
    ) -> ArtistModel:
        try:
            profile = {k: v for k, v in profile.dict().items() if v is not None}
            await self.db["artists"].update_one({"_id": id}, {"$set": profile})
            model = await self.get_profile(id)
            return model
        except Exception as e:
            msg = f"[UPDATE_PROFILE] Profile: {profile} error: {e}"
            logging.error(msg)
            raise RuntimeError(msg)