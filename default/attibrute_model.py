from enum import Enum
from dataclasses import dataclass
from typing import Union, Optional, Any, List, TypeVar, Type, Callable, cast

import env
import server

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TypeEnum(Enum):
    boolean = "boolean"
    email = "email"
    integer = "integer"
    string = "string"
    float = "float"
    date = "date"


@dataclass
class AttributeModel:
    collection: str
    key: str
    type: TypeEnum
    required: Optional[bool] = False
    default: Optional[Union[float, str, int]] = None
    size: Optional[int] = None
    array: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AttributeModel':
        assert isinstance(obj, dict)
        collection = from_str(obj.get("collection"))
        key = from_str(obj.get("key"))
        type = TypeEnum(obj.get("type"))
        required = from_bool(obj.get("required"))
        default = from_union([from_float, from_str, from_none], obj.get("default"))
        size = from_union([from_int, from_none], obj.get("size"))
        return AttributeModel(collection, key, type, required, default, size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["type"] = to_enum(TypeEnum, self.type)
        result["required"] = from_bool(self.required)
        if self.default is not None:
            result["default"] = from_union([to_float, from_str, from_none], self.default)
        if self.size is not None:
            result["size"] = from_union([from_int, from_none], self.size)
        return result

    def created(self):
        try:
            server.databases.get_attribute(env.db, self.collection, self.key)
            print(f" ✓ attribute {self.key}")
        except:
            attribute_creators = {
                TypeEnum.string: server.databases.create_string_attribute,
                TypeEnum.float: server.databases.create_float_attribute,
                TypeEnum.integer: server.databases.create_integer_attribute,
                TypeEnum.boolean: server.databases.create_boolean_attribute,
                TypeEnum.email: server.databases.create_email_attribute,
                TypeEnum.date: server.databases.create_datetime_attribute
            }
            attribute_creator = attribute_creators.get(self.type)
            if attribute_creator:
                kwargs = {
                    'database_id': env.db,
                    'collection_id': self.collection,
                    'key': self.key,
                    'default': self.default,
                    'required': self.required,
                    'array': self.array
                }
                if self.type in [TypeEnum.string]:
                    kwargs['size'] = self.size
                attribute_creator(**kwargs)
                print(f" 🆕 attribute {self.key}")


