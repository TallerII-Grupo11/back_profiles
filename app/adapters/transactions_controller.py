from fastapi import APIRouter, status

from app.db import DatabaseManager, get_database
from app.db.impl.transaction_manager import TransactionManager
from app.db.model.transaction import TransactionModel, UpdateTransactionModel

router = APIRouter(tags=["transactions"])


@router.get(
    "/transactions",
    response_description="Get all transactions",
    status_code=status.HTTP_200_OK,
)
async def get(
    db: DatabaseManager = Depends(get_database),
):
    manager = TransactionsManager(db.db)
    try:
        model = await manager.get_all()
        return model
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Could not get transations. Exception: {e}"
        )


@router.post(
    "/transactions",
    response_description="Create transaction",
    status_code=status.HTTP_200_OK,
)
async def post(
    req: TransactionModel = Body(...),
    db: DatabaseManager = Depends(get_database),
):
    manager = TransactionsManager(db.db)
    try:
        model = await manager.add(req)
        return model
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Could not create transactions. Exception: {e}"
        )


@router.put(
    "/transactions/{id}",
    response_description="Update transaction",
    status_code=status.HTTP_200_OK,
)
async def update(
    id: str,
    req: UpdateTransactionModel = Body(...),
    db: DatabaseManager = Depends(get_database),
):
    manager = TransactionsManager(db.db)
    try:
        model = await manager.update(id, req)
        return model
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Could not update transactions. Exception: {e}"
        )