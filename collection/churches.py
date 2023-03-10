import env
from default.attibrute_model import AttributeModel, TypeEnum
from default.collection_model import CollectionModel
from default import permissoes, tipo_index, ordem
from default.index_model import IndexModel


def created():
    collection = 'churches'
    CollectionModel(database=env.db, collection=collection, permission=permissoes.admin_owner, documentSecurity=True
                    ).created()

    AttributeModel(collection=collection, key='name', type=TypeEnum.string, size=256, required=True).created()
    AttributeModel(collection=collection, key='fantasyName', type=TypeEnum.string, size=256, required=True).created()
    AttributeModel(collection=collection, key='cpfCnpj', type=TypeEnum.string, size=20, required=True).created()
    AttributeModel(collection=collection, key='status', type=TypeEnum.boolean, required=True).created()
    AttributeModel(collection=collection, key='zipCode', type=TypeEnum.string, size=15, required=True).created()
    AttributeModel(collection=collection, key='city', type=TypeEnum.string, size=60, required=True).created()
    AttributeModel(collection=collection, key='uf', type=TypeEnum.string, size=2, required=True).created()
    AttributeModel(collection=collection, key='district', type=TypeEnum.string, size=256, required=True).created()
    AttributeModel(collection=collection, key='street', type=TypeEnum.string, size=256, required=True).created()
    AttributeModel(collection=collection, key='number', type=TypeEnum.string, size=20, required=True).created()
    AttributeModel(collection=collection, key='complement', type=TypeEnum.string, size=256, required=True).created()
    AttributeModel(collection=collection, key='contact', type=TypeEnum.string, size=256, required=True).created()
    AttributeModel(collection=collection, key='email', type=TypeEnum.email, required=False).created()
    AttributeModel(collection=collection, key='phone1', type=TypeEnum.string, size=20, required=True).created()
    AttributeModel(collection=collection, key='phone2', type=TypeEnum.string, size=20, required=False).created()
    AttributeModel(collection=collection, key='facebook', type=TypeEnum.string, size=150, required=False).created()
    AttributeModel(collection=collection, key='instagram', type=TypeEnum.string, size=80, required=False).created()
    AttributeModel(collection=collection, key='youtube', type=TypeEnum.string, size=80, required=False).created()
    AttributeModel(collection=collection, key='site', type=TypeEnum.string, size=100, required=False).created()
    AttributeModel(collection=collection, key='tiktok', type=TypeEnum.string, size=30, required=False).created()
    AttributeModel(collection=collection, key='churchHeadId', type=TypeEnum.string, size=45, required=False).created()
    AttributeModel(collection=collection, key='responsibleId', type=TypeEnum.string, size=45, required=True).created()

    IndexModel(collection=collection, key='name', type=tipo_index.fulltext, attributes=['name'],
               orders=ordem.asc).created()
    IndexModel(
        collection=collection, key='fantasyName', type=tipo_index.fulltext, attributes=['fantasyName'], orders=ordem.asc) \
        .created()
    IndexModel(
        collection=collection, key='cpfCnpj', type=tipo_index.key, attributes=['cpfCnpj'], orders=ordem.asc).created()
    IndexModel(
        collection=collection, key='churchHeadId', type=tipo_index.key, attributes=['churchHeadId'],
        orders=ordem.asc).created()
    IndexModel(
        collection=collection, key='city', type=tipo_index.fulltext, attributes=['city'], orders=ordem.asc).created()
    IndexModel(collection=collection, key='uf', type=tipo_index.fulltext, attributes=['uf'], orders=ordem.asc).created()

