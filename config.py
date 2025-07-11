from os import getenv
from dotenv import load_dotenv

load_dotenv()

token = getenv('TOKEN')
admins = {int(x) for x in (getenv('ADMINS').split(","))}