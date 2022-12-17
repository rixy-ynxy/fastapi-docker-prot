from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserInDB

CREATE_USER_QUERY = """
    INSERT INTO users (name, description, age, color_type)
    VALUES (:name, :description, :age, :color_type)
    RETURNING id, name, description, age, color_type;
"""

GET_USER_BY_ID_QUERY = """
SELECT id, name, description, age, color_type
FROM users
WHERE id = :id;
"""



class UsersRepository(BaseRepository):
    async def create_cleaning(self, *, new_user: UserCreate) -> UserInDB:
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
