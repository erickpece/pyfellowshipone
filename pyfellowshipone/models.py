# -*- coding: utf-8 -*-

"""
pyfellowshipone.models
~~~~~~~~~~~~~~~~~~~~

This module contains Fellowship One API Objects.
"""

import json


class Person(object):
    __attrs__ = [
        'id',
        'household_id',
        'first_name',
        'last_name',
        'date_of_birth',
        'gender'
    ]

    def __init__(self, json="", id=0, first_name="", last_name="", household_id="", date_of_birth="", gender=""):
        # If no JSON data has been specified, populate by individual parameters
        if json == "":
            self.id = id
            self.household_id = household_id
            self.first_name = first_name
            self.last_name = last_name
            self.date_of_birth = date_of_birth
            self.gender = gender
            return

        # If we're here, there has been some data passed in via JSON.  Let's get
        # to work!
        self.id = json['@id']
        self.household_id = json['@householdID']
        self.first_name = json['firstName']
        self.last_name = json['lastName']
        self.date_of_birth = json['dateOfBirth']
        self.gender = json['gender']

    def describe(self):
        return "%s: %s %s" % (self.id, self.first_name, self.last_name)

    def json(self):
        return json.dumps(self.__dict__)