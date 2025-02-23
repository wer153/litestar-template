from litestar import Litestar
from litestar.di import Provide

from litestar_project.repository.base import postgres

from .api.system import ENDPOITNS as ENDPOINTS_SYSTEM
from .api.model import ENDPOINTS as ENDPOINTS_MODEL


def create_app():
    return Litestar(
        route_handlers=[
            *ENDPOINTS_SYSTEM,
            *ENDPOINTS_MODEL,
        ],
        dependencies={"prisma": Provide(postgres)},
    )
