from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.models.user import UserCreate, UserPublic
from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserInDB
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND


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

@router.get("/{id}/", response_model=UserPublic,
                name="users:get-user-by-id")
async def get_user_by_id(
  id: int, users_repo: UsersRepository = Depends(
    get_repository(UsersRepository
    ))
) -> UserPublic:
  user = await users_repo.get_user_by_id(id=id)
  if not user:
    raise HTTPException(
      status_code=HTTP_404_NOT_FOUND,
      detail="指定されたidのユーザーは見つかりませんでした"
    )
    return user

CREATE_USER_QUERY = """
  INSERT INTO user (name, description, age, color_type)
  VALUES (:name, :description, :age, :color_type)
  RETURNING id, name, description, age, color_type;
"""
GET_USER_BY_ID_QUERY = """
  SELECT id, name, description, age, color_type
  FROM users
  WHERE id = :id;
"""

class UserRepository(BaseRepository):
  async def create_user(self, *, new_user: UserCreate) -> UserInDB:
    query_values = new_user.dict()
    user = await self.db.fetch_one(
      query=CREATE_USER_QUERY,
      values=query_values
    )
    return UserInDB(**user)
  async def get_user_by_id(self, *, id: int) -> UserInDB:
    user = await self.db.fetch_one(
      query=GET_USER_BY_ID_QUERY,
      values={"id": id}
    )
    if not user:
      return None
    return UserInDB(**user)
