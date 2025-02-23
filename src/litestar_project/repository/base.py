from typing import TypeVar, Generic, ClassVar, get_args, Type
from collections.abc import Sequence
from pydantic import BaseModel
from prisma import Prisma

T = TypeVar("T", bound=BaseModel)


async def postgres():
    db = Prisma()
    await db.connect()
    yield db
    await db.disconnect()


class PrismaRepository(Generic[T]):
    _model_name: ClassVar[str] = ""
    _model_type: Type[T]

    def __init__(self, prisma: Prisma) -> None:
        self._prisma = prisma
        # Get the model type from the generic parameter
        self._model_type = get_args(self.__class__.__orig_bases__[0])[0]  # type: ignore
        # Set the model name if not explicitly defined
        if not self.__class__._model_name:
            self.__class__._model_name = self._model_type.__name__.lower()
        self._model = getattr(self._prisma, self.__class__._model_name)

    async def create(self, data: T) -> T:
        """Create a new record"""
        return await self._model.create(data=data.model_dump(exclude_unset=True))

    async def get_by_id(self, id: str) -> T | None:
        """Get a record by ID"""
        return await self._model.find_unique(where={"id": id})

    async def get_all(self, skip: int = 0, take: int = 100) -> Sequence[T]:
        """Get all records with pagination"""
        return await self._model.find_many(skip=skip, take=take)

    async def update(self, id: str, data: T) -> T | None:
        """Update a record by ID"""
        return await self._model.update(
            where={"id": id}, data=data.model_dump(exclude_unset=True)
        )

    async def delete(self, id: str) -> T | None:
        """Delete a record by ID"""
        return await self._model.delete(where={"id": id})

    async def count(self) -> int:
        """Get total count of records"""
        return await self._model.count()

    async def find_many(
        self, where: dict, skip: int = 0, take: int = 100
    ) -> Sequence[T]:
        """Find many records with filter"""
        return await self._model.find_many(where=where, skip=skip, take=take)

    async def find_first(self, where: dict) -> T | None:
        """Find first record matching filter"""
        return await self._model.find_first(where=where)

    async def upsert(self, where: dict, create: T, update: T) -> T:
        """Create or update a record"""
        return await self._model.upsert(
            where=where,
            create=create.model_dump(exclude_unset=True),
            update=update.model_dump(exclude_unset=True),
        )

    async def create_many(self, data: Sequence[T]) -> int:
        """Create multiple records"""
        return await self._model.create_many(
            data=[item.model_dump(exclude_unset=True) for item in data]
        )

    async def update_many(self, where: dict, data: T) -> int:
        """Update multiple records"""
        return await self._model.update_many(
            where=where, data=data.model_dump(exclude_unset=True)
        )

    async def delete_many(self, where: dict) -> int:
        """Delete multiple records"""
        return await self._model.delete_many(where=where)
