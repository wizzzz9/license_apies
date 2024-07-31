import uuid
from fastapi import HTTPException


async def is_valid_uuid4(uuid_string):
    try:
        uuid.UUID(uuid_string, version=4)
    except ValueError:
        raise HTTPException(status_code=401, detail="License key is not valid or expired")