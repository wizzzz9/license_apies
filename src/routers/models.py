import time
from datetime import datetime

from pydantic import BaseModel


class CheckLicenseResponseModel(BaseModel):
    status: bool = True


class CreateUserPayload(BaseModel):
    username: str
    license_time: datetime = None
    user_info: str = None
    role_id: int = 3

class CreateUserResponseModel(BaseModel):
    username: str
    licence_key: str



