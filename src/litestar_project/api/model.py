from collections.abc import Sequence
from uuid import uuid4
from litestar import get, post
from prisma import Prisma
from prisma.models import model
from litestar_project.router import Endpoint
from litestar_project.repository.model import ModelRepository
from pydantic import BaseModel


class ModelCreateDTO(BaseModel):
    name: str

    class Config:
        from_attributes = True


@get("/models")
async def _list_models(prisma: Prisma) -> Sequence[model]:
    repo = ModelRepository(prisma)
    return await repo.get_all()


@post("/models")
async def _create_model(data: ModelCreateDTO, prisma: Prisma) -> model:
    repo = ModelRepository(prisma)
    model_data = model(id=str(uuid4()), **data.model_dump())
    return await repo.create(model_data)


ENDPOINTS = Endpoint(
    [_list_models, _create_model],
)
