from pydantic import Field
from app.db.model.py_object_id import PyObjectId
from pydantic.main import BaseModel
from typing import Optional
from bson import ObjectId


class TransactionModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sender: str = Field(...)
    receiver: str = Field(...)
    amount: float = Field(...)
    date: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "sender": "wallet_addr",
                "receiver": "wallet_addr",
                "amount": 3.4,
                "date": "20/07/2022"
            }
        }


class UpdateTransactionModel(BaseModel):
    sender: Optional[str]
    receiver: Optional[str]
    amount: Optional[float]
    date: Optional[str]
