from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.models.user import UserCreate, UserPublic
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

router = APIRouter()

@router.get("/")
async def get_all_users() -> List[dict]:
  users = [
    {"id": 1, "name": "momo", "color": "SALT & PEPPER", "age": 2},
    {"id": 2, "name": "coco", "color": "DARK GREY", "age": 1.5}
  ]

  return users

@router.post("/",
            response_model=UserPublic,
            name="users:create-user",
            status_code=HTTP_201_CREATED)
async def create_new_user(
  new_user: UserCreate = Body(..., embed=True),
  users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
  ) -> UserPublic:
  created_user = await users_repo.create_user(new_user=new_user)
  return created_user
