# -*- coding: utf-8 -*-

"""
pyfellowshipone.session
~~~~~~~~~~~~~~~~~~~~

This module contains the session handler for Fellowship One.
"""

import os
import json
import rauth
import urllib
import urlparse

from base64 import b64encode
from rauth import OAuth1Service, OAuth1Session

import httplib

class F1Session(OAuth1Session):

	"""
	Creates a Fellowship One Session using OAuth1Session from rauth
	"""

	def hash_credentials(self, username, password):
		credentials = b64encode( "%s %s" % ( username, password ) )
		credentials = urllib.quote_plus( credentials )

		return credentials

	def __init__(self, consumerKey, consumerSecret, username, password, churchCode, staging = False):
		self.consumerKey = consumerKey
		self.consumerSecret = consumerSecret
		self.username = username
		self.password = password
		self.churchCode = churchCode
		self.staging = staging

		if self.staging:
			self.url = "https://%s.fellowshiponeapi.com/" % self.churchCode
		else:
			self.url = "https://%s.staging.fellowshiponeapi.com/" % self.churchCode

		self.authenticate()

	def patch_send(self):
	    old_send= httplib.HTTPConnection.send
	    def new_send( self, data ):
	        print data
	        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
	    httplib.HTTPConnection.send= new_send

	def authenticate(self):
		credentials = self.hash_credentials(self.username, self.password)

		service = OAuth1Service (
			consumer_key = self.consumerKey,
			consumer_secret = self.consumerSecret,
			request_token_url = "%sv1/PortalUser/AccessToken" % self.url
		)

		tokens = service.get_raw_request_token(data = credentials)
		tokens_content = urlparse.parse_qs(tokens.content)

		oauth_token = tokens_content['oauth_token'][0]
		oauth_tokensecret = tokens_content['oauth_token_secret'][0]

		# Add debug logging here to display credentials and tokens

		session = OAuth1Session (
			self.consumerKey,
			self.consumerSecret,
			oauth_token,
			oauth_tokensecret
		)

		self.session = session

	# Strips any leading forward slashes from the endpoint
	def clean_endpoint(self, endpoint):
		return endpoint.lstrip('//')

	def get(self, endpoint, **kwargs):
		# Enable next line for debugging
		# self.patch_send()
		request_url = "%s%s" % (self.url, self.clean_endpoint(endpoint))

		# print "Starting request %s with %s" % (request_url,)

		return self.session.get(request_url, header_auth=True, headers={"Accept": "application/json"}, **kwargs)

	def post(self, endpoint, **kwargs):
		# Enable next line for debugging
		# self.patch_send()

		request_url = "%s%s" % (self.url, self.clean_endpoint(endpoint))

		return self.session.post(request_url, header_auth=False, headers={"Accept": "application/json", "Content-type": "application/json"}, **kwargs)