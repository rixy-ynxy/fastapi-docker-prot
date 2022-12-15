from enum import Enum
from typing import Optional

from app.models.core import CoreModel, IDModelMixin


class ColorType(str, Enum):
	solt_and_pepper = "SOLT & PEPPER"
	dark_grey = "DARK GREY"
	chocolate = "CHOCOLATE"


class UserBase(CoreModel):
  name: Optional[str]
  description: Optional[str]
  age: Optional[float]
  color_type: Optional[ColorType]


class UserCreate(UserBase):
  name: str
  color_type: ColorType


class UserUpdate(UserBase):
  description: str
  age: float


class UserInDB(IDModelMixin, UserBase):
    name: str
    age: float
    color_type: ColorType


class UserPublic(IDModelMixin, UserBase):
    pass
