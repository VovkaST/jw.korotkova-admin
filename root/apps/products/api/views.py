from root.apps.products.application.boundaries.dtos import ProductDTO
from root.apps.products.application.controllers import ProductController
from root.contrib.openapi.views import AutoSchema
from root.contrib.rest.decorators import action
from root.core.api.views import APIViewSet


class ProductViewSet(APIViewSet):
    schema = AutoSchema(tags=["products"], operation_id_base="")

    product_controller = ProductController()

    @action(url_name="products_in_stock", url_path="in_stock", response_schema=list[ProductDTO])
    async def get_products_in_stock(self, request, *args, **kwargs):
        return await self.product_controller.get_products_in_stock()
