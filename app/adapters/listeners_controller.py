from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.impl.listener_manager import ListenerManager
from app.db.model.listener import ListenerModel, UpdateListenerModel

router = APIRouter(tags=["listeners"])


@router.post(
    "/listeners/{user_id}",
    response_description="Add new listener profile",
    response_model=ListenerModel
)
async def create_profile(
    user_id: str,
    db: DatabaseManager = Depends(get_database)
):
    manager = ListenerManager(db.db)
    created_profile = await manager.add_profile(user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)


@router.get(
    "/listeners/{user_id}",
    response_description="Get a single listener profile",
    response_model=ListenerModel,
    status_code=status.HTTP_200_OK,
)
async def show_profile(user_id: str, db: DatabaseManager = Depends(get_database)):
    manager = ListenerManager(db.db)
    profile = await manager.get_profile(user_id=user_id)
    if profile is not None:
        return profile
    raise HTTPException(status_code=404,
                        detail=f"Listener's Profile {user_id} not found"
                        )


@router.put(
    "/listeners/{user_id}",
    response_description="Update a listener's profile",
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    id: str,
    listener: UpdateListenerModel = Body(...),
    db: DatabaseManager = Depends(get_database)
):
    manager = ListenerManager(db.db)
    response = manager.update_profile(listener=listener)
    if response:
        return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content={"message": f"Success update of profile {id}"}
                            )

    raise HTTPException(status_code=404,
                        detail=f"Listener's Profile {id} not found"
                        )
