import logging
from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Body

from app.db.model.listener import ListenerModel, UpdateListenerModel
from fastapi.encoders import jsonable_encoder


class ListenerManager:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_profile(self, id: str) -> ListenerModel:
        profile = await self.db["listeners"].find_one({"_id": id})
        return profile

    async def get_all_profiles(self, user_id: str) -> List[ListenerModel]:
        if user_id is not None:
            profiles = (
                await self.db["listeners"].find({"user_id": user_id}).to_list(100)
            )
        else:
            profiles = await self.db["listeners"].find().to_list(100)

        return profiles

    async def get_profile_by_user_id(self, user_id: str) -> ListenerModel:
        profile = await self.db["listeners"].find_one({"user_id": user_id})
        return profile

    async def add_profile(self, listener: ListenerModel = Body(...)):
        profile = jsonable_encoder(listener)
        await self.db["listeners"].insert_one(profile)
        return profile

    async def delete_profile(self, id: str):
        delete_result = await self.db["listeners"].delete_one({"_id": id})
        return delete_result

    async def update_profile(
        self, id: str, profile: UpdateListenerModel = Body(...)
    ) -> ListenerModel:
        try:
            profile = {k: v for k, v in profile.dict().items() if v is not None}
            await self.db["listeners"].update_one({"_id": id}, {"$set": profile})
            model = await self.get_profile(id)
            return model
        except Exception as e:
            msg = f"[UPDATE_PROFILE] Profile: {profile} error: {e}"
            logging.error(msg)
            raise RuntimeError(msg)
