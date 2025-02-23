from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient
from unittest import mock


async def test_test(app: Litestar):
    async with AsyncTestClient(app) as client:
        response = await client.get("/models")
    assert response.status_code == HTTP_200_OK
    assert response.json() == []


async def test_create_model(app: Litestar):
    async with AsyncTestClient(app) as client:
        with mock.patch(
            "litestar_project.api.model.uuid4",
            return_value="392da63d-bf59-4242-9142-e551c05544eb",
        ):
            response = await client.post("/models", json={"name": "test"})
    # breakpoint()
    assert response.status_code == HTTP_201_CREATED
    assert {"name": "test"}.items() <= response.json().items()
