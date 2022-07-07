import unittest
import pytest
from unittest.mock import MagicMock

from app.db.impl.listener_manager import ListenerManager
from app.db.model.listener import ListenerModel
from app.db.model.py_object_id import PyObjectId


class TestListenerManager(unittest.TestCase):
    db = MagicMock()

    @pytest.mark.asyncio
    async def test_get_profile(self):
        listener = ListenerModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            user_id="user_id"
        )
        self.db["listeners"].find_one = MagicMock(return_value=listener)

        listener_manager = ListenerManager(self.db)
        result = await listener_manager.get_profile("62be27922d98b5aaad951f95")
        self.assertIsNotNone(result)

    @pytest.mark.asyncio
    async def test_get_all_profiles_with_user_id_filter(self):
        listener = ListenerModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            user_id="user_id"
        )
        self.db["listeners"].find.to_list = MagicMock(return_value=[listener])

        listener_manager = ListenerManager(self.db)
        result = await listener_manager.get_all_profiles("user_id")
        self.assertTrue(len(result) == 1)

    @pytest.mark.asyncio
    async def test_get_all_profiles(self):
        listener = ListenerModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            user_id="user_id"
        )
        listener2 = ListenerModel(
            _id=PyObjectId("62be27922d98b5aaad951f96"),
            user_id="another_one"
        )
        self.db["listeners"].find.to_list = MagicMock(return_value=[listener, listener2])

        listener_manager = ListenerManager(self.db)
        result = await listener_manager.get_all_profiles(user_id=None)
        self.assertTrue(len(result) == 2)

    @pytest.mark.asyncio
    async def test_delete(self):
        self.db["listeners"].delete_one = MagicMock(return_value=True)
        listener_manager = ListenerManager(self.db)
        result = await listener_manager.delete_profile("id")
        self.assertTrue(result)
