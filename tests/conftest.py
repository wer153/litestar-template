import pytest

from litestar_project.app import create_app


@pytest.fixture(autouse=True, scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def app():
    return create_app()
