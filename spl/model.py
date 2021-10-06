import typing

_NULL = object()


class Attribute:
    __slots__ = (
        "_default",
    )

    def __init__(
        self,
        default: typing.Any = _NULL,
    ) -> None:
        self._default = default

    @property
    def default(self) -> typing.Any:
        if callable(self._default):
            return self._default()

        return self._default

    def __get__(self, *_) -> typing.Any:
        ...

    def __set__(*_) -> None:
        raise AttributeError("you can't set an Model attribute, "
                             "use an Entry to edit a Model instance")


class ModelMeta(type):
    def __len__(self) -> int:
        return 0


class Model(metaclass=ModelMeta):
    __models__: typing.ClassVar[dict[str, type["Model"]]] = {}

    def __init_subclass__(cls, **options: typing.Any) -> None:
        self: type[Model] = Model

        if cls.__base__ != self:  # type: ignore
            raise RuntimeError("you can't subclass a Model")

        name = options.pop("name", cls.__name__)
        self.__models__[name] = cls

        for identifier, annotation in cls.__annotations__.items():
            error = None

            if isinstance(annotation, str):
                error = "str annotations is not supported "
            elif annotation not in {str, int, float}:
                error = f"{annotation!r} is not a supported annotation"

            if error:
                raise RuntimeError(f"{cls.__name__}.{identifier}: {error}")

            default = getattr(cls, identifier, _NULL)
            descriptor = Attribute(default)

            setattr(cls, identifier, descriptor)
