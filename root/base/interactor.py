from root.contrib.clean_architecture.utils import create_dto_object


class BaseInteractor:
    @staticmethod
    async def entity_to_dto(dto_class, entity_object, mappings: dict = None, exclude: list = None):
        return await create_dto_object(dto_class, entity_object, mappings=mappings, exclude=exclude)

    @staticmethod
    async def entities_to_dtos(dto_class, entity_objects, mappings: dict = None, exclude: list = None):
        return [
            await create_dto_object(dto_class, entity_object, mappings=mappings, exclude=exclude)
            for entity_object in entity_objects
        ]
