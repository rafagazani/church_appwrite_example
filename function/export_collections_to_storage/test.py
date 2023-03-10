import json
import env
from export_collections_to_storage import main


class RequestModel:
    variables = {}
    payload = {}

    def teste(self):
        pass

    def get_json(self):
        return json.dumps(self.variables)

    def json(self, resp):
        print(json.dumps(resp))

    def send(self, test):
        print(test)


request = RequestModel()

data = json.dumps({})

request.payload = data

request.variables["host"] = env.host
request.variables["projeto"] = env.project
request.variables["db"] = env.db
request.variables["key"] = env.function_key
request.variables['APPWRITE_FUNCTION_EVENT_DATA'] = data
response = RequestModel()

main(request, response)
