from datetime import datetime
from pydantic import BaseModel
from uuid import UUID



class CreateUserPayload(BaseModel):
    username: str
    license_time: datetime = None
    user_info: str = None
    role_id: int = 3


class RenewLicensePayload(BaseModel):
    user_license_key: str
    license_time: datetime = None


class CheckLicenseResponseModel(BaseModel):
    status: bool = True


class RenewLicenseResponseModel(BaseModel):
    status: bool = True
    username: str
    expiry_license: datetime


class CreateUserResponseModel(BaseModel):
    username: str
    license_key: str | UUID
