import requests
from sqlalchemy import *

db = create_engine("postgresql://fortnoxDB:14kdvKsI7IfeFfwn@35.195.0.180/postgres")
metadata = MetaData(db)
db_obj = Table('Api_credential', metadata, autoload=True)
ins = db_obj.select()
result = ins.execute().fetchall()

print result