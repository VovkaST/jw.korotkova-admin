import pathlib


def upload_product_file_to(instance, filename: str) -> str:
    """Build path to store concrete product's file"""
    path = pathlib.Path("products") / str(instance.product.guid) / filename
    return str(path)
