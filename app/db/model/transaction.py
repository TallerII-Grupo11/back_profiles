from pydantic import Field

from pydantic.main import BaseModel


class TransactionModel(BaseModel):
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
                "sender": "id",
                "receiver": "name",
                "amount": 3.0,
                "date": "name"
            }
        }
