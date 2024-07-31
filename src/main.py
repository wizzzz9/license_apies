from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routers.license_router import check_license_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin',
                   "Set-Cookie", "Authorization"]
)



app.include_router(check_license_router, prefix="/api")
