from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from order_service.router import router as order_router


app = FastAPI(title="Order microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router)
