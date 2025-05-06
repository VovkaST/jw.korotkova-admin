from decimal import Decimal

from pydantic import UUID4, BaseModel, Field, NonNegativeInt


class ProductChannelPublicationCreateDTO(BaseModel):
    product_id: int
    channel_id: int
    message_id: int
    text: str
    is_main: bool = Field(default=False)


class ProductChannelPublicationUpdateDTO(BaseModel):
    text: str | None = Field(default=None)
    is_main: bool | None = Field(default=None)


class ProductTypeDTO(BaseModel):
    id: NonNegativeInt
    name: str
    description: str | None = Field(default=None)
    is_active: bool


class ProductFileDTO(BaseModel):
    id: NonNegativeInt
    file: str
    description: str | None = Field(default=None)


class ProductDTO(BaseModel):
    guid: UUID4
    type: ProductTypeDTO
    type_id: int
    title: str
    description: str
    price: Decimal
    in_stock: bool
    files: list[ProductFileDTO] = Field(default_factory=list)
