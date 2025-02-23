from dataclasses import dataclass
from ..router import Endpoint
from litestar import get


@dataclass
class HealthCheckResponse:
    status: str


@get("/healthcheck")
async def _healthcheck() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")


ENDPOITNS = Endpoint(
    hanlders=[
        _healthcheck,
    ],
)
