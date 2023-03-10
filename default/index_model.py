from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast

import env
import server

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class IndexModel:
    collection: str
    key: str
    type: str
    orders: List[str]
    attributes: List[str]
    database: Optional[str] = env.db

    @staticmethod
    def from_dict(obj: Any) -> 'IndexModel':
        assert isinstance(obj, dict)
        database = from_str(obj.get("databases"))
        collection = from_str(obj.get("collection"))
        type = from_str(obj.get("type"))
        key = from_str(obj.get("key"))
        orders = from_list(from_str, obj.get("orders"))
        attributes = from_list(from_str, obj.get("attributes"))
        return IndexModel(collection, type, key, orders, attributes, database)

    def to_dict(self) -> dict:
        result: dict = {}
        result["databases"] = from_str(self.database)
        result["collection"] = from_str(self.collection)
        result["type"] = from_str(self.type)
        result["key"] = from_str(self.key)
        result["orders"] = from_list(from_str, self.orders)
        result["attributes"] = from_list(from_str, self.attributes)
        return result

    def created(self):
        itens = server.databases.list_indexes(self.database, self.collection)
        for index in itens["indexes"]:
            if index["key"] == self.key:
                print(f" \u2713 index {self.key}")
                break
        else:
            print(f"  Criando o index {self.key}...")
            server.databases.create_index(database_id=self.database,
                                          collection_id=self.collection,
                                          key=self.key,
                                          type=self.type,
                                          attributes=self.attributes,
                                          orders=self.orders)
            print(f"   \U0001F195 index {self.key} --OK--")


def index_model_from_dict(s: Any) -> IndexModel:
    return IndexModel.from_dict(s)


def index_model_to_dict(x: IndexModel) -> Any:
    return to_class(IndexModel, x)
