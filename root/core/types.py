from typing import TypeAlias

from root.core.enums import ImageSizesChoices

ThumbnailImageSize: TypeAlias = tuple[int, int] | int
ThumbnailSizes: TypeAlias = dict[ImageSizesChoices, ThumbnailImageSize]

DeleteResult: TypeAlias = tuple[int, dict[str, int]]
