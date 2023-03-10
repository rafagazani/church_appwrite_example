import json
from appwrite.client import Client
from appwrite.input_file import InputFile
from appwrite.query import Query
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
import xlsxwriter

# appwrite functions createDeployment --functionId=export_collections_to_storage --activate=true --entrypoint="export_collections_to_storage.py" --code="."

databases: Databases
database_id = ''
storage: Storage
payload = {}


def main(request, response):
    initialize_appwrite(request, response)

    collections = databases.list_collections(database_id)

    for collection in collections['collections']:
        all_docs = get_all_documents(collection["$id"], [])
        file_name = f'{collection["$id"]}.xlsx'
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        if len(all_docs) == 0:
            workbook.close()
            upload_file(file_name)
            continue

        headers = [header for header in all_docs[0].keys()]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        for row, document in enumerate(all_docs, start=1):
            permissions_str = ", ".join(document["$permissions"])
            document["$permissions"] = permissions_str
            for col, header in enumerate(headers):
                worksheet.write(row, col, document[header])

        workbook.close()
        upload_file(file_name)

    return response.send(f"collections:{len(collections['collections'])}")


def upload_file(file_name):
    storage.create_file('collections', "unique()", InputFile.from_path(file_name))


def get_all_documents(collection_id, queries):
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
