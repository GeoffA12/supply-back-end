import http.server
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import mysql.connector as sqldb
import requests

# from dispatch import Dispatch
# import datetime

ver = '0.3.0'


def connectToSQLDB():
    return sqldb.connect(user = 'root', password = 'password', database = 'team22supply', port = 6022)

