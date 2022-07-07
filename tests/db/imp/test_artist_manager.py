import unittest
import pytest
from unittest.mock import MagicMock

from app.db.impl.artist_manager import ArtistManager
from app.db.model.artist import ArtistModel
from app.db.model.py_object_id import PyObjectId


class TestArtistManager(unittest.TestCase):
    db = MagicMock()

    @pytest.mark.asyncio
    async def test_get_profile(self):
        artist = ArtistModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            user_id="user_id"
        )
        self.db["artists"].find_one = MagicMock(return_value=artist)

        artist_manager = ArtistManager(self.db)
        result = await artist_manager.get_profile("62be27922d98b5aaad951f95")
        self.assertIsNotNone(result)

    @pytest.mark.asyncio
    async def test_get_all_profiles_with_user_id_filter(self):
        artist = ArtistModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            user_id="user_id"
        )
        self.db["artists"].find.to_list = MagicMock(return_value=[artist])

        artist_manager = ArtistManager(self.db)
        result = await artist_manager.get_all_profiles("user_id")
        self.assertTrue(len(result) == 1)

    @pytest.mark.asyncio
    async def test_get_all_profiles(self):
        artist = ArtistModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            user_id="user_id"
        )
        artist2 = ArtistModel(
            _id=PyObjectId("62be27922d98b5aaad951f96"),
            user_id="another_one"
        )
        self.db["artists"].find.to_list = MagicMock(return_value=[artist, artist2])

        artist_manager = ArtistManager(self.db)
        result = await artist_manager.get_all_profiles(user_id=None)
        self.assertTrue(len(result) == 2)

    @pytest.mark.asyncio
    async def test_delete(self):
        self.db["artists"].delete_one = MagicMock(return_value=True)
        artist_manager = ArtistManager(self.db)
        result = await artist_manager.delete_profile("id")
        self.assertTrue(result)
