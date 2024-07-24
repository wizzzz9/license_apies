from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session, User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import UUID4

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]


def validate_license_key(license_key: UUID4, db: Session = Depends(db_dependency)):
    user = db.query(User).filter(User.licence_key == license_key).first()
    if user is None:
        raise HTTPException(status_code=404, detail="License key not found")
    if user.license_time and user.license_time > datetime.utcnow():
        return user
    else:
        raise HTTPException(status_code=400, detail="License key is not valid or expired")
