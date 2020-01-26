import pymongo
 
my_client = pymongo.MongoClient(
    "mongodb+srv://admin:openSourceTextbooks@slybrary-jbhct.gcp.mongodb.net/test?retryWrites=true&w=majority"
)

try:
    print("MongoDB version is %s" %
            my_client.server_info()['version'])
except pymongo.errors.OperationFailure as error:
    print(error)
    quit(1)