import my_appwrite

timeout = 900


def deploy_all():
    created_wipe_all_documents_from_a_collection()
    created_export_collections_to_storage()


def created_wipe_all_documents_from_a_collection():
    my_appwrite.set_funcao('wipe_all_documents_from_a_collection', timeout=timeout)


def created_export_collections_to_storage():
    my_appwrite.set_funcao('export_collections_to_storage', timeout=timeout)
