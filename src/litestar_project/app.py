from litestar import Litestar
from .api.system import ENDPOITNS as ENDPOINTS_SYSTEM


def create_app():
    return Litestar(
        route_handlers=[
            *ENDPOINTS_SYSTEM,
        ],
    )
