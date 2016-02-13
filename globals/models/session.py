from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import py_path
from global_settings import Settings

settings = Settings()


db_data = settings.DATABASES['default']
db_uri = db_data['URI']

connection_params = {}
if 'SA' in db_data:
    connection_params.update(db_data['SA'])
engine = create_engine(db_uri, **connection_params)
Session = sessionmaker(bind=engine)

session = Session()


