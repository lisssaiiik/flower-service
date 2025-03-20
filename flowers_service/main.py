from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flowers_service.router import router as flowers_router


app = FastAPI(title="Flowers microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flowers_router)
