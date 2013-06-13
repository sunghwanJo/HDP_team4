#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'

def db_set():
	db.create_all()
	parsing_data.db_insert_cafe()
	parsing_data.db_insert_facebook()
	print "SUCCESS!!!"
