from ..router import Endpoint
from litestar import get


@get("/healthcheck")
def _healthcheck() -> str:
    return "OK"


ENDPOITNS = Endpoint(
    hanlders=[
        _healthcheck,
    ],
)
