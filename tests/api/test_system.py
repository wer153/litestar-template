from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient


async def test_healthcheck(app: Litestar):
    async with AsyncTestClient(app) as client:
        response = await client.get("/healthcheck")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"status": "ok"}
