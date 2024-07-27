from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from src.database import User
from src.dependencies import db_dependency, validate_license_key, validate_admin_key
from src.routers.models import CreateUserPayload

check_license_router = APIRouter(
    prefix='/license',
    tags=['License']
)


@check_license_router.get("/check_license")
async def check_license(license_key: str, user: User = Depends(validate_license_key)):
    return {"valid": True}


@check_license_router.post("/create_user")
async def create_user(admin_key: str, payload: CreateUserPayload, db: db_dependency,
                      admin: User = Depends(validate_admin_key)):
    result = await db.execute(select(User).filter(User.username == payload.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    if payload.license_time is None:
        payload.license_time = datetime.utcnow() + timedelta(days=30)

    new_user = User(
        username=payload.username,
        license_time=payload.license_time,
        user_info=payload.user_info,
        role_id=payload.role_id
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "key": new_user.licence_key}
