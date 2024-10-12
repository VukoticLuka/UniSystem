import json
import os

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


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
    payload = data["case_create"]["paylod"]

    response = await async_client.post("/student", json=payload)

    assert response.status_code == 201
