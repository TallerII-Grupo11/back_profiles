from pydantic import Field
from app.db.model.py_object_id import PyObjectId

from pydantic.main import BaseModel
from typing import Optional

class TransactionModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sender: str = Field(...)
    receiver: str = Field(...)
    amount: float = Field(...)
    date: str = Field(...)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "sender": "wallet_id",
                "receiver": "wallet_id",
                "amount": 3.0,
                "date": "name"
            }
        }


class UpdateTransactionModel(BaseModel):
    sender: Optional[str]
    receiver: Optional[str]
    amount: Optional[float]
    date: Optional[str]

    