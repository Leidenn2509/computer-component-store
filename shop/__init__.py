from flask import Flask
import psycopg2

DB = "postgres"
HOST = "127.0.0.1"
USER = "postgres"
PWD = "postgres"

app = Flask(__name__)
conn = psycopg2.connect(dbname=DB, user=USER, password=PWD, host=HOST)