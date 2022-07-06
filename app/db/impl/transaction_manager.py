import logging
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Body

from app.db.model.transaction import TransactionModel, UpdateTransactionModel
from fastapi.encoders import jsonable_encoder


class TransactionManager:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get(self, id: str):
        model = await self.db["transactions"].find_one({"_id": id})
        return model

    async def add(self, transaction: TransactionModel = Body(...)):
        model = jsonable_encoder(transaction)
        await self.db["transactions"].insert_one(model)
        return model

    async def update(self, id: str, transaction: UpdateTransactionModel = Body(...)):
        try:
            model = {k: v for k, v in transaction.dict().items() if v is not None}
            await self.db["transactions"].update_one({"_id": id}, {"$set": model})
            model = await self.get(id)
            return model
        except Exception as e:
            msg = f"[UPDATE_PROFILE] transaction: {transaction} error: {e}"
            logging.error(msg)
            raise RuntimeError(msg)

    async def get_all(self):
        models = await self.db["transactions"].find().to_list(100)
        return models