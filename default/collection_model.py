from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast

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


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


@dataclass
class CollectionModel:
    database: str
    collection: str
    permission: str
    documentSecurity: bool

    @staticmethod
    def from_dict(obj: Any) -> 'CollectionModel':
        assert isinstance(obj, dict)
        database = from_str(obj.get("databases"))
        collection = from_str(obj.get("collection"))
        permission = from_str(obj.get("permission"))
        documentSecurity = from_bool(obj.get("documentSecurity"))
        return CollectionModel(database, collection, permission, documentSecurity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["databases"] = from_str(self.database)
        result["collection"] = from_str(self.collection)
        result["permission"] = from_str(self.permission)
        return result

    def created(self):
        try:
            print(f"verificando se existe a coleção {self.collection}")
            server.databases.get_collection(self.database, self.collection)
            print(f"\u2713 coleção {self.collection}")
        except:
            print(f"Criando a coleção {self.collection}...")
            server.databases.create_collection(database_id=self.database,
                                                 name=self.collection,
                                                 collection_id=self.collection,
                                                 permissions=self.permission,
                                                 document_security=self.documentSecurity)
            print(f" \U0001F195 coleção {self.collection} --OK--")


def collection_model_from_dict(s: Any) -> CollectionModel:
    return CollectionModel.from_dict(s)


def collection_model_to_dict(x: CollectionModel) -> Any:
    return to_class(CollectionModel, x)
