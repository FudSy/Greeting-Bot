from os import getenv
from dotenv import load_dotenv

load_dotenv()

token = getenv('TOKEN')
admins = {int(x) for x in (getenv('ADMINS').split(","))}
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': getenv('DB_PASSWORD'),
    'db': getenv('DB_NAME'),
}