# -*- coding: utf-8 -*-

"""

pyfellowshipone.auth
~~~~~~~~~~~~~~~~~~~~

This module contains the authentication handler for Fellowship One.

"""

import os
import rauth
import urllib
import urlparse

from base64 import b64encode
from rauth import OAuth1Service, OAuth1Session

class F1Session(OAuth1Session):
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
			self.url = "https://%s.fellowshiponeapi.com/v1/" % self.churchCode
		else:
			self.url = "https://%s.staging.fellowshiponeapi.com/v1/" % self.churchCode

		credentials = self.hash_credentials(username, password)

		service = OAuth1Service (
			consumer_key = self.consumerKey,
			consumer_secret = self.consumerSecret,
			request_token_url = "%sPortalUser/AccessToken" % self.url
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

	def get(self, resource, parameters=""):
		request_url = "%s%s" % (self.url, resource)

		return self.session.get(request_url, headers={"Accept": "application/json"}, params=parameters)