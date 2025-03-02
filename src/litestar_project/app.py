from litestar import Litestar
from litestar.di import Provide

from litestar_project.repository.base import postgres
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import StoplightRenderPlugin

from .api.system import ENDPOITNS as ENDPOINTS_SYSTEM
from .api.model import ENDPOINTS as ENDPOINTS_MODEL


def create_app():
    return Litestar(
        route_handlers=[
            *ENDPOINTS_SYSTEM,
            *ENDPOINTS_MODEL,
        ],
        dependencies={"prisma": Provide(postgres)},
        openapi_config=OpenAPIConfig(
            title="Project Name",
            description="Project Description",
            version="0.0.1",
            render_plugins=[StoplightRenderPlugin()],
        ),
    )
