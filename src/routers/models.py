import time
from datetime import datetime

from pydantic import BaseModel


class CreateUserPayload(BaseModel):
    username: str
    license_time: datetime = None
    user_info: str = None
    role_id: int = 3
