from typing import Union

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.models.course import Semester


class DbCourse(BaseModel):
    name: str = Field(min_length=3)
    espb: int = Field(gt=1, lt=20)
    semester: Semester = Field(default=Semester.FIRST.value)
    study_year: int = Field(ge=1, le=6)

    @field_validator("name")
    def check_name(cls, value: str):
        if not value[0].isupper():
            raise ValueError("First character must be Upper letter")
        return value


class CourseDisplay(DbCourse):
    course_id: int

    model_config = ConfigDict(extra="forbid",
                              from_attributes=True,
                              use_enum_values=False)


class CourseUpdate(BaseModel):
    name: Union[str, None] = Field(default=None)
    espb: Union[int, None] = Field(default=None)
    semester: Union[Semester, None] = Field(default=None)
    study_year: Union[int, None] = Field(default=None)

    @field_validator("study_year")
    def check_study_year(cls, value):
        if value < 1 or value > 6:
            raise ValueError("Study year must be between 1 and 6")
        return value
