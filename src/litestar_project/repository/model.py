from litestar_project.repository.base import PrismaRepository
from prisma.models import model


class ModelRepository(PrismaRepository[model]): ...
