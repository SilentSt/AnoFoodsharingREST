import databases
import sqlalchemy
from settings import settings


DATABASE_URL = settings.POSTGRES_CDN

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
