from __future__ import annotations

from collections.abc import Callable, Sequence

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from easy_thumbnails.engine import generate_source_image
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.namers import source_hashed

from root.apps.products.application.boundaries.dtos import ProductFileCreateDTO
from root.apps.products.application.boundaries.product import IProductRepository
from root.apps.products.application.domain.entities import ProductEntity
from root.apps.products.models import Product, ProductFiles
from root.base.entity import ImageMeta
from root.base.repository import BaseRepository
from root.contrib.clean_architecture.interfaces import ObjectId
from root.core.enums import FileTypesChoices, ImageSizesChoices
from root.core.types import ThumbnailSizes


class ProductRepository(BaseRepository, IProductRepository):
    model = Product
    product_file_model = ProductFiles
    base_entity_class = ProductEntity

    def get_queryset(self):
        return super().get_queryset().select_related("type").prefetch_related("files")

    async def get_products(self, product_ids: list[ObjectId]) -> Sequence[ProductEntity]:
        """Get all given products"""
        publications = self.get_queryset().filter(id__in=product_ids)
        return await self.to_entities(self.base_entity_class, publications)

    async def get_products_in_stock(self) -> Sequence[ProductEntity]:
        qs = self.get_queryset().filter(in_stock=True)
        return await self.to_entities(self.base_entity_class, qs)

    async def add_images(
        self, product_id: ObjectId, files: list[ProductFileCreateDTO], sizes: ThumbnailSizes | None = None
    ) -> Sequence[ObjectId]:
        product = await self.model.objects.aget(id=product_id)
        instances = []
        ids = []
        for dto in files:
            instance = self.product_file_model(product=product)
            upload_path = self.product_file_model.file.field.upload_to(instance, dto.file.name)
            images = await self.make_thumbnails(File(dto.file), relative_name=upload_path, sizes=sizes)
            parent = None
            for path, meta in images:
                if meta.size_code == ImageSizesChoices.ORIGINAL:
                    parent = instance
                    instance.file = path
                    instance.type = FileTypesChoices.IMAGE
                    instance.meta = meta.model_dump()
                    instance.description = dto.description
                    await instance.asave()
                    ids.append(instance.pk)
                else:
                    instance = self.product_file_model(
                        product=product,
                        parent=parent,
                        file=path,
                        type=FileTypesChoices.IMAGE,
                        meta=meta.model_dump(),
                        description=dto.description,
                    )
                    instances.append(instance)
        await self.product_file_model.objects.abulk_create(instances, batch_size=20)
        ids.extend([instance.pk for instance in instances])
        return ids

    async def make_thumbnails(
        self, obj, relative_name: str, sizes: ThumbnailSizes | None = None, namer: Callable = source_hashed, crop=True
    ) -> list[tuple[str, ImageMeta]]:
        sizes = sizes or {}
        thumbnailer = get_thumbnailer(obj, relative_name=relative_name)
        thumbnailer.thumbnail_namer = namer

        source_image = generate_source_image(
            thumbnailer, thumbnailer.get_options({}), thumbnailer.source_generators, fail_silently=False
        )
        H = source_image.height
        W = source_image.width

        files = []
        file = default_storage.save(relative_name, obj)
        files.append((file, ImageMeta(size=f"{W}x{H}", size_code=ImageSizesChoices.ORIGINAL, length=obj.size)))

        for size_code, size in sizes.items():
            if isinstance(size, int):
                if W < H:
                    if size > H:
                        continue
                    size = (0, size)
                elif W > H:
                    if size > W:
                        continue
                    size = (size, 0)
                else:
                    if H == W == size:
                        continue
                    size = (size, size)
            else:
                width, height = size
                if width >= W and height >= H:
                    continue
                size = min([width, W]), min([height, H])

            thumb = thumbnailer.generate_thumbnail({"size": size, "crop": crop})
            thumb_content = thumb.read()
            file = default_storage.save(thumb.name, ContentFile(thumb_content))
            files.append(
                (file, ImageMeta(size=f"{thumb.width}x{thumb.height}", size_code=size_code, length=thumb.size))
            )

        return files
