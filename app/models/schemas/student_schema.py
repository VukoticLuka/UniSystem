from typing import Literal, Union

from pydantic import BaseModel, Field, EmailStr, AliasGenerator, ConfigDict, field_validator, ValidationError
from ..student_model import Level


class DbStudent(BaseModel):
    username: str = Field(min_length=8, max_length=20)
    email: EmailStr = Field(default="user@example.com")
    firstname: str
    lastname: str
    level: Level = Field(default=Level.BACHELOR, validate_default=True)

    @field_validator("level")
    def check_level(cls, value):
        if value not in Level.__members__.values():
            raise ValueError("Level must be: bachelor, master or doctoral")
        return value


class StudentDisplay(DbStudent):
    id: int

    model_config = ConfigDict(str_strip_whitespace=True,
                              extra="forbid", use_enum_values=True,
                              from_attributes=True)


class StudentUpdate(BaseModel):
    username: Union[str | None] = Field(default=None)
    email: Union[EmailStr | None] = Field(default=None)
    firstname: str | None = None
    lastname: str | None
    level: Union[Level | None] = Field(default=None)

    @field_validator("username")
    def check_username(cls, value):
        if value is not None and len(value) not in range(8, 21):
            raise ValueError("Username must be at least 8 and at most 20 characters")
        return value




