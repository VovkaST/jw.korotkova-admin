from typing import Literal, TypeAlias, TypedDict, TypeVar


class BaseDict(TypedDict, total=False):
    pass


DTO = TypeVar("DTO", bound=BaseDict)
Entity = TypeVar("Entity")
OrderBy: TypeAlias = dict[str, Literal["asc", "desc"]]
ObjectId: TypeAlias = int | str
