from appwrite.services.account import Account
from appwrite.services.functions import Functions
from appwrite.services.storage import Storage
from appwrite.services.teams import Teams
from appwrite.services.users import Users

import env
from appwrite.client import Client
from appwrite.services.databases import Databases

client = Client()

(client
 .set_endpoint(env.host)
 .set_project(env.project)
 .set_key(env.key)
 )

databases = Databases(client)
try:
    databases.get(env.db)

except:
    databases.create(env.db, env.db)

storage = Storage(client)
functions = Functions(client)
teams = Teams(client)
account = Account(client)
users = Users(client)
