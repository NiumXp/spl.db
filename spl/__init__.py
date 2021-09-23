import typing

T = typing.TypeVar('T', bound="Model")


class _attribute:
    __slots__ = ()

    def __init__(self) -> None:
        pass

    def __get__(self, *_) -> typing.Any:
        ...

    def __set__(*_) -> None:
        raise AttributeError("you can't set this attribute")


class Model:
    __models__: typing.ClassVar[dict[str, type[T]]] = {}

    def __init_subclass__(cls, **options) -> None:
        self: type[Model] = Model

        if cls.__base__ != self:
            raise RuntimeError("you can't subclass a Model")

        name = options.pop("name", cls.__name__)
        self.__models__[name] = cls

        for identifier, annotation in cls.__annotations__.items():
            ...

            descriptor = _attribute()
            setattr(cls, identifier, descriptor)
