from typing import Optional, Union, Generic, Type

from fastapi import HTTPException, status
from app.core.base import ModelGen


class EntityNotFound(HTTPException, Generic[ModelGen]):
    def __init__(self, model_class: Type[ModelGen], entity_data: Union[str, int]):
        status_code = status.HTTP_404_NOT_FOUND
        detail = f"{model_class.__name__} "
        if isinstance(entity_data, int):
            detail += f"with ID {entity_data} not found"
        else:
            detail += f"with NAME or EMAIL {entity_data} not found"
        super().__init__(status_code=status_code, detail=detail)


class EntityAlreadyExists(HTTPException, Generic[ModelGen]):
    def __init__(self, model_class: Type[ModelGen], entity_data: Union[str, int]):
        status_code = status.HTTP_409_CONFLICT
        detail = f"{model_class.__name__} "
        if isinstance(entity_data, int):
            detail += f"with ID {entity_data} already exists"
        else:
            detail += f"with NAME or EMAIL {entity_data} already exists"
        super().__init__(status_code=status_code, detail=detail)
