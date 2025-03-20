from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cart_service.router import router as cart_router
from cart_service.router import stars_router as star_router

app = FastAPI(title="Cart microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cart_router)
app.include_router(star_router)