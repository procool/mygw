from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import py_path
from global_settings import Settings

settings = Settings()


db_data = settings.DATABASES['default']
db_uri = db_data['URI']

db_echo = False
if 'ECHO' in db_data:
    db_echo = db_data['ECHO']
 
engine = create_engine(db_uri, echo=db_echo)
Session = sessionmaker(bind=engine)

session = Session()


