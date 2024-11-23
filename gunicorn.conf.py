import multiprocessing
import os

from dotenv import load_dotenv

load_dotenv(override=True)

bind = os.getenv("GUNICORN_DOMAIN")
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
cache = None
reload = False
wsgi_app = "core.wsgi:application"

accesslog = "logs/gunicorn/gunicorn_access.log"
errorlog = "logs/gunicorn/gunicorn_error.log"
loglevel = "debug"
