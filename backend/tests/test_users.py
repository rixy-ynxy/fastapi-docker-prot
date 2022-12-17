import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from app.models.user import UserCreate, UserInDB
from starlette.status import (HTTP_200_OK,
                              HTTP_201_CREATED,
                              HTTP_404_NOT_FOUND,
                              HTTP_422_UNPROCESSABLE_ENTITY)

pytestmark = pytest.mark.asyncio

@pytest.fixture
def new_user():
  return UserCreate(
    name="test user",
    description="test description",
    age=0.0,
    color_type="SOLT & PEPPER",
  )

class TestUsersRoutes:
  async def test_routes_exist(
      self,
      app: FastAPI,
      client: AsyncClient
  ) -> None:
      res = await client.post(app.url_path_for("users:create-user"), json={})
      assert res.status_code != HTTP_404_NOT_FOUND

  async def test_invalid_input_raises_error(
      self,
      app: FastAPI,
      client: AsyncClient
  ) -> None:
      res = await client.post(app.url_path_for("users:create-user"), json={})
      assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

class TestCreateUser:
  async def test_valid_input_creates_user(
    self,
    app: FastAPI,
    client: AsyncClient,
    new_user: UserCreate
  ) -> None:
    res = await client.post(
      app.url_path_for("users: create-user"),
      json={"new_user": new_user.dictU()}
    )
    assert res.status_code == HTTP_201_CREATED
    created_user = UserCreate(**res.json())
    assert created_user == new_user

  @pytest.mark.parametrize(
    "invalid_payload, status_code",
    (
      (None, 422),
      ({}, 422),
      ({"name": "test_name"}, 422),
      ({"age": 2}, 422),
      ({"name": "test_name", "description": "test"}, 422),
    ),
  )
  async def test_invalid_input_raises_error(
    self,
    app: FastAPI,
    client: AsyncClient,
    invalid_payload: dict,
    status_code: int
  ) -> None:
    res = await client.post(
      app.url_path_for("users:create-user"),
      json={"new_user": invalid_payload}
    )
    assert res.status_code == status_code

class TestGetUser:
  async def test_get_user_by_id(
      self,
      app: FastAPI,
      client: AsyncClient,
      test_user: UserInDB
  ) -> None:
      res = await client.get(app.url_path_for(
          "users:get-user-by-id",
          id=test_user.id
      ))
      assert res.status_code == HTTP_200_OK
      user = UserInDB(**res.json())
      assert user == test_user

  @pytest.mark.parametrize(
      "id, status_code",
      (
          (500, 404),
          (-1, 404),
          (None, 422),
      ),
  )
  async def test_wrong_id_returns_error(
      self, app: FastAPI, client: AsyncClient, id: int, status_code: int
  ) -> None:
    res = await client.get(app.url_path_for("users:get-user-by-id", id=id))
    assert res.status_code == status_code
