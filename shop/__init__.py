from flask import Flask
from flask_httpauth import HTTPBasicAuth
import psycopg2

DB = "postgres"
HOST = "127.0.0.1"
USER = "postgres"
PWD = "postgres"

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin"

app = Flask(__name__)
auth = HTTPBasicAuth()
conn = psycopg2.connect(dbname=DB, user=USER, password=PWD, host=HOST)