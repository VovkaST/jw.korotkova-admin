from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps


class InterceptError:
    @staticmethod
    def redirect(from_error: type[Exception], to_error: type[Exception]):
        async def decorator(method: Callable) -> Callable:
            @wraps(method)
            async def wrapper(self, *args, **kwargs):
                try:
                    if inspect.iscoroutinefunction(method):
                        return await method(self, *args, **kwargs)
                    return method(self, *args, **kwargs)
                except from_error:
                    raise to_error

            return wrapper

        return decorator

    @staticmethod
    def swallow(exception: type[Exception] | tuple[Exception]):
        async def decorator(method: Callable) -> Callable:
            @wraps(method)
            async def wrapper(self, *args, **kwargs):
                try:
                    if inspect.iscoroutinefunction(method):
                        return await method(self, *args, **kwargs)
                    return method(self, *args, **kwargs)
                except exception:
                    pass

            return wrapper

        return decorator

    @staticmethod
    def allow_does_not_exists(method: Callable) -> Callable:
        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            try:
                if inspect.iscoroutinefunction(method):
                    return await method(self, *args, **kwargs)
                return method(self, *args, **kwargs)
            except self.mode.DoesNotExist:
                pass

        return wrapper
