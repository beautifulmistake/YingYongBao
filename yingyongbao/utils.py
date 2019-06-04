import pymongo

from yingyongbao.settings import MONGO_URL, MONGO_DB_NAME, MONGO_IP, MONGO_PORT


def get_db():
    # mongo_uri = 'mongodb://wb_zyym:orange123@39.105.31.96:27017/all_project_xxc'
    # mongo_db = pymongo.MongoClient(mongo_uri)
    # return mongo_db.get_database("all_project_xxc")

    # mongo_client = pymongo.MongoClient(MONGO_IP, MONGO_PORT)
    # return mongo_client[MONGO_DB_NAME]
    mongo_db = pymongo.MongoClient(MONGO_URL)
    return mongo_db[MONGO_DB_NAME]
