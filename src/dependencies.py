from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session, User
from fastapi import Depends, HTTPException
from datetime import datetime
from src.utils import is_valid_uuid4

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]


async def validate_license_key(license_key: str, db: db_dependency) -> User:
    await is_valid_uuid4(uuid_string=license_key)
    result = await db.execute(select(User).filter(User.licence_key == license_key))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="License key not found")
    if user.license_time and user.license_time > datetime.utcnow():
        return user
    else:
        raise HTTPException(status_code=401, detail="License key is not valid or expired")


async def validate_admin_key(admin_key: str, db: db_dependency) -> User:
    await is_valid_uuid4(uuid_string=admin_key)
    result = await db.execute(select(User).filter(User.licence_key == admin_key))
    user = result.scalars().first()
    if user.role_id != 1:
        raise HTTPException(status_code=403, detail="User is not an admin")
    if user is None:
        raise HTTPException(status_code=404, detail="License key not found")
    if user.license_time and user.license_time > datetime.utcnow():
        return user
    else:
        raise HTTPException(status_code=401, detail="License key is not valid or expired")
