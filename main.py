import functions
import my_appwrite
from collection import churches

my_appwrite.login_cli()
churches.created()
functions.deploy_all()
