import unittest
import pytest
from unittest.mock import MagicMock

from app.db.impl.transaction_manager import TransactionManager
from app.db.model.transaction import TransactionModel
from app.db.model.py_object_id import PyObjectId


class TestTransactionManager(unittest.TestCase):
    db = MagicMock()

    @pytest.mark.asyncio
    async def test_get(self):
        transaction = TransactionModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            sender="asd",
            receiver="fgh",
            amount=123,
            date="01/01/2022"
        )
        self.db["transactions"].find_one = MagicMock(return_value=transaction)

        transaction_manager = TransactionManager(self.db)
        result = await transaction_manager.get("62be27922d98b5aaad951f95")
        self.assertIsNotNone(result)

    @pytest.mark.asyncio
    async def test_get_all_profiles(self):
        transaction = TransactionModel(
            _id=PyObjectId("62be27922d98b5aaad951f95"),
            sender="asd",
            receiver="fgh",
            amount=123,
            date="01/01/2022"
        )
        transaction2 = TransactionModel(
            _id=PyObjectId("62be27922d98b5aaad951f96"),
            sender="qwe",
            receiver="asd",
            amount=12,
            date="02/01/2022"
        )
        self.db["transactions"].find.to_list = MagicMock(return_value=[transaction, transaction2])

        transaction_manager = TransactionManager(self.db)
        result = await transaction_manager.get_all_profiles(user_id=None)
        self.assertTrue(len(result) == 2)
