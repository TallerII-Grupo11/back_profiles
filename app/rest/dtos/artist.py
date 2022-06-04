from pydantic import Field

from pydantic.main import BaseModel


class ArtistModel(BaseModel):
    artist_id: str = Field(...)
    artist_name: str = Field(...)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "artist_id": "id",
                "artist_name": "name",
            }
        }
