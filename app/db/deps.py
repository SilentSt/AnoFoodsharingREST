from datetime import timedelta
from typing import Any

import sqlalchemy
from ormar.fields.model_fields import ModelFieldFactory
from ormar.fields.base import BaseField


class Interval(ModelFieldFactory, timedelta):

    _type = timedelta
    _sample = timedelta(minutes=0)

    def __new__(  # type: ignore # noqa CFQ002
        cls, *, minutes: int = 0, **kwargs: Any
    ) -> BaseField:  # type: ignore
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.Interval()