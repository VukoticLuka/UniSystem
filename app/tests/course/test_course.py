import os
import json

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.models.schemas.course_schema import DbCourse


def load_course_data():
    curr_dir = os.path.dirname(__file__)

    path = os.path.join(curr_dir, "data.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file {path} not found")

    with open(path, "r") as f:
        data = json.load(f)

    return data


data = load_course_data()


@pytest.mark.asyncio
async def test_course_creation(
        async_client: AsyncClient,
        async_session: AsyncSession
):
    payload = data["case_create"]["payload"]
    response = await async_client.post("/course/", json=DbCourse(**payload).model_dump())

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_course_already_exists(
        async_client: AsyncClient,
        async_session: AsyncSession
):
    payload = data["case_create"]["payload"]

    async with async_session.begin():
        async_session.add(Course(**payload))
        await async_session.flush()

    response = await async_client.post("/course/", json=DbCourse(**payload).model_dump())

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_course_fetching(
        async_client: AsyncClient,
        async_session: AsyncSession
):
    payload = data["case_create"]["payload"]

    async with async_session.begin():
        async_session.add(Course(**payload))
        await async_session.flush()

    name = data["case_get"]["want"]["name"]

    response = await async_client.get(f"/course/{name}")

    assert response.status_code == 200
    assert response.json()["name"] == name


@pytest.mark.asyncio
async def test_delete_course(
        async_client: AsyncClient,
        async_session: AsyncSession
):
    payload = data["case_create"]["payload"]

    async with async_session.begin():
        async_session.add(Course(**payload))
        await async_session.flush()

    name = data["case_delete"]["want"]["name"]

    response = await async_client.delete(f"/course/{name}")

    assert response.status_code == 200
    assert response.json()["name"] == name


@pytest.mark.asyncio
async def test_delete_not_existing_course(
        async_client: AsyncClient,
        async_session: AsyncSession
):
    name = data["case_delete"]["want"]["name"]

    response = await async_client.delete(f"/course/{name}")

    assert response.status_code == 404
