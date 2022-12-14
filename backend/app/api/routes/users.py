from typing import List
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_all_users() -> List[dict]:
    users = [
        {"id": 1, "name": "momo", "color": "SALT & PEPPER", "age": 2},
        {"id": 2, "name": "coco", "color": "DARK GREY", "age": 1.5}
    ]

    return users
