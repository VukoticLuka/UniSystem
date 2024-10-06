from typing import Literal, Union

from pydantic import BaseModel, Field, EmailStr, AliasGenerator, ConfigDict, field_validator, ValidationError
from ..student_model import Level


class DbStudent(BaseModel):
    username: str = Field(min_length=8, max_length=20)
    email: EmailStr = Field(default="user@example.com")
    firstname: str
    lastname: str
    level: Level = Field(default=Level.BACHELOR.value)

    @field_validator("level")
    def check_level(cls, value):
        if value not in Level.__members__.values():
            raise ValueError("Level must be: bachelor, master or doctoral")
        return value


class StudentDisplay(DbStudent):
    id: int

    model_config = ConfigDict(str_strip_whitespace=True,
                              extra="forbid", use_enum_values=False,
                              from_attributes=True)


class StudentUpdate(BaseModel):
    email: Union[EmailStr | None] = Field(default=None)
    firstname: str | None = None
    lastname: str | None = None
    level: Union[Level | None] = Field(default=None)




