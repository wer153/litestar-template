from litestar_project.repository.base import PrismaRepository
from prisma import Prisma
from prisma.models import model
from prisma.actions import modelActions


class TestRepositoryWithoutModelName(PrismaRepository[model]): ...


class TestRepositoryWithModelName(PrismaRepository[model]):
    _model_name = "model"


def test_model_name(prisma: Prisma):
    repo = TestRepositoryWithoutModelName(prisma)
    assert repo._model_name == "model"
    assert isinstance(repo._model, modelActions)


def test_model_name2(prisma: Prisma):
    repo = TestRepositoryWithModelName(prisma)
    assert repo._model_name == "model"
    assert isinstance(repo._model, modelActions)
