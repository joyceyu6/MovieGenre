#! /usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/')
from application import app as application
application.secret_key = 'Joyce Genre Movie project secret key'
