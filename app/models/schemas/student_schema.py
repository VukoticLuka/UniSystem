from typing import Literal, Union, Optional

from pydantic import BaseModel, Field, EmailStr, AliasGenerator, ConfigDict, field_validator, ValidationError
from ..student import Level, Gender

from datetime import datetime


class DbStudent(BaseModel):
    username: str = Field(min_length=8, max_length=20)
    email: EmailStr = Field(default="user@example.com")
    firstname: str
    lastname: str
    index_number: int = Field(ge=1)
    enrollment_year: int
    gender: Optional[Gender] = Field(default=None)
    education: Optional[Level] = Field(default=Level.BACHELOR.value)

    @field_validator("education")
    def check_level(cls, value):
        if value not in Level.__members__.values():
            raise ValueError("Level must be: bachelor, master or doctoral")
        return value

    @field_validator("enrollment_year")
    def check_enrollment_year(cls, value):
        curr_year = datetime.now().year
        if value > curr_year or value < curr_year - 10:
            raise ValueError(f"Enrollment year mus be between {curr_year - 10} and {curr_year}")
        return value


class StudentDisplay(DbStudent):
    id: int

    model_config = ConfigDict(str_strip_whitespace=True,
                              extra="forbid", use_enum_values=False,
                              from_attributes=True)


class StudentUpdate(BaseModel):
    email: Union[EmailStr, None] = Field(default=None)
    firstname: Union[str, None] = Field(default=None)
    lastname: Union[str, None] = Field(default=None)
    index_number: Union[int, None] = Field(default=None)
    enrollment_year: Union[int, None] = Field(default=None)
    gender: Union[Gender, None] = Field(default=None)
    education: Union[Level, None] = Field(default=None)
