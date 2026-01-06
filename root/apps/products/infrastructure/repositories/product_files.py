from root.apps.products.application.boundaries.product_files import IProductFilesRepository
from root.apps.products.application.domain.entities import ProductFileEntity
from root.apps.products.models import ProductFiles
from root.base.repository import BaseRepository


class ProductFilesRepository(BaseRepository, IProductFilesRepository):
    model = ProductFiles
    base_entity_class = ProductFileEntity
