import json
from appwrite.client import Client
from appwrite.query import Query
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage

# appwrite functions createDeployment --functionId=wipe_all_documents_from_a_collection --activate=true --entrypoint="wipe_all_documents_from_a_collection.py" --code="."

databases: Databases
database_id = ''
storage: Storage
payload = {}


def main(request, response):
    initialize_appwrite(request, response)

    for collection in payload:
        all_docs = get_all_documents(collection, [])

        if len(all_docs) == 0:
            continue

        for document in all_docs:
            delete_document(collection, document["$id"])

    return response.send(f"collections:{payload}")


def get_all_documents(collection_id, queries):
    try:
        databases.get_collection(database_id, collection_id, )
    except:
        return []

    documents = databases.list_documents(database_id, collection_id, )
    itens = documents['documents']
    while len(documents['documents']) > 0:
        fil = queries
        fil.append(Query.cursorAfter(documents['documents'][len(documents['documents']) - 1]["$id"]))
        fil.append(Query.limit(100))
        documents = databases.list_documents(database_id, collection_id, queries=fil, )
        itens += documents['documents']
        fil.clear()
    return itens


def delete_document(collection_id, document_id):
    try:
        databases.delete_document(database_id, collection_id, document_id)
    except:
        pass


def initialize_appwrite(request, response):
    if request.variables.get('host', '') == '':
        return response.send('coloque o host nas variáveis', 500)
    if request.variables.get('projeto', '') == '':
        return response.send('coloque o projeto nas variáveis', 500)
    if request.variables.get('key', '') == '':
        return response.send('coloque o key nas variáveis', 500)
    if request.variables.get('db', '') == '':
        return response.send('coloque o db nas variáveis', 500)

    client = Client()
    client.set_endpoint(request.variables.get('host', ''))
    client.set_project(request.variables.get('projeto', ''))
    client.set_key(request.variables.get('key', ''))

    global database_id
    database_id = request.variables.get('db', '')

    global databases
    databases = Databases(client)
    global storage
    storage = Storage(client)

    global payload
    payload = json.loads(request.variables['APPWRITE_FUNCTION_EVENT_DATA'] or "{}")

    try:
        storage.get_bucket("collections")
    except:
        storage.create_bucket("collections", "collections")
