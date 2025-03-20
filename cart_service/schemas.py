from pydantic import BaseModel 


class SStars(BaseModel):
    """Избранное"""
    id: int
    bouquet_id: int
    user_id: int

