from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from src.database import User
from src.dependencies import db_dependency, validate_license_key, validate_admin_key, validate_admin_key_dependency, \
    validate_license_key_dependency
from src.routers.models import CreateUserPayload, CheckLicenseResponseModel, CreateUserResponseModel, \
    RenewLicensePayload, RenewLicenseResponseModel

check_license_router = APIRouter(
    prefix='/license',
    tags=['License']
)


@check_license_router.get("/check_license")
async def check_license(user: validate_license_key_dependency) -> CheckLicenseResponseModel:
    return CheckLicenseResponseModel()


@check_license_router.post("/create_user")
async def create_user(payload: CreateUserPayload, db: db_dependency,
                      admin: validate_admin_key_dependency) -> CreateUserResponseModel:
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
    return CreateUserResponseModel(username=new_user.username,
                                   licence_key=new_user.licence_key)


@check_license_router.post("/renew_license", description="If license_time is None it will automatically set utcnow + 30 days")
async def renew_license(payload: RenewLicensePayload, db: db_dependency,
                        admin: validate_admin_key_dependency
                        ) -> RenewLicenseResponseModel:
    result = await db.execute(select(User).filter(User.licence_key == payload.user_licence_key))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.license_time is None:
        user.license_time = datetime.utcnow() + timedelta(days=30)
    else:
        user.license_time = payload.license_time
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return RenewLicenseResponseModel(valid=True, expiry_license=user.license_time)
