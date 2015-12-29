import cron.py_path
from global_settings import Settings

settings = Settings()

for attr in dir(settings):
    if attr.startswith('_'):
        continue
    print attr, getattr(settings, attr)
