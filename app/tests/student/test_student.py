import json
import os

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.student_schema import DbStudent
from app.models.student import Student


def load_student_data() -> dict:
    curr_dir = os.path.dirname(__file__)

    path = os.path.join(curr_dir, "data.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file {path} not found")

    with open(path, "r") as f:
        data = json.load(f)

    return data


data = load_student_data()


@pytest.mark.asyncio
async def test_create_student(
        async_client: AsyncClient,
        async_session: AsyncSession
):
    payload = data["case_create"]["payload"]
    response = await async_client.post("/student/", json=DbStudent(**payload).dict())

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_student(async_client: AsyncClient,
                           async_session: AsyncSession):
    payload = data["case_create"]["payload"]

    async with async_session.begin():
        student = Student(**payload)
        async_session.add(student)
        await async_session.flush()
    username = data["case_get"]["want"]

    response = await async_client.get(f"/student/{username['username']}")

    assert response.status_code == 200

    assert response.json()["username"] == username['username']


@pytest.mark.asyncio
async def test_check_health(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json()["msg"] == "Ok"
