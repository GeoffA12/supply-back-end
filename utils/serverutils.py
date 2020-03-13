import http.server
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import mysql.connector as sqldb
import requests

# from dispatch import Dispatch
# import datetime

ver = '0.2'


def connectToSQLDB():
    return sqldb.connect(user = 'root', password = 'password', database = 'team22demand', port = 6022)

def getPOSTBody():
    length = int(BaseHTTPRequestHandler.headers['content-length'])
    body = BaseHTTPRequestHandler.rfile.read(length)
    return json.loads(body)
