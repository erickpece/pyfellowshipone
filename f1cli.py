# -*- coding: utf-8 -*-

"""
pyfellowshipone.f1cli
~~~~~~~~~~~~~~~~~~~~

This module allows for command line interaction with the Fellowship One API.
"""

import os
import yaml

from pyfellowshipone.session import F1Session
from pyfellowshipone.models import Person

# Load configuration file
dir = os.path.realpath('.')

config_filename = os.path.join(dir, "config.yml")
config = yaml.load(file(config_filename))

auth_settings = config['authentication']['staging']

session = F1Session(
	auth_settings['key'], 
	auth_settings['secret'], 
	auth_settings['username'], 
	auth_settings['password'], 
	auth_settings['church_code']
)

payload = {'communication': 'EMAIL'}
people = session.get('People/Search', payload).json()['results']

for p in people['person']:
	person = Person(json=p)

	print person.json()