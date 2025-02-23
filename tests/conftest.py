import pytest

from litestar_project.app import create_app
from prisma import Prisma


@pytest.fixture(autouse=True, scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture(scope="function")
async def prisma():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()


@pytest.fixture(autouse=True, scope="function")
async def cleanup(prisma: Prisma):
    models = [prisma.model]
    for model in models:
        await model.delete_many()
    yield
