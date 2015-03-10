import os
import re
import json
import yaml
import collections
import urllib
import pprint

from rauth import *
from base64 import b64encode


class ResponseObject:
	def __init__(self, **kwargs):
		self.success = kwargs.get('success', False)
		self.result = kwargs.get('result', '')
		self.message = kwargs.get('message', '')
		self.model = kwargs.get('model', '')

	def __str__(self):
		response = collections.OrderedDict()
		response['success'] = str(self.success)
		response['message'] = str(self.message)

		try:
			response['result'] = "{}: {}".format(self.result.reason, self.result.text)
		except:
			response['result'] = str(self.result)

		return json.dumps(response)


class F1Session(OAuth1Session):


	"""
	Creates a Fellowship One Session using OAuth1Session from rauth
	"""

	def hash_credentials(self, username, password):
		credential_string = "{} {}".format(username, password)
		credentials = b64encode(bytes(credential_string, "utf-8"))
		credentials = urllib.parse.quote_plus( credentials )

		return credentials

	def __init__(self, consumerKey, consumerSecret, username, password, url):
		self.consumerKey = consumerKey
		self.consumerSecret = consumerSecret
		self.username = username
		self.password = password
		self.url = url

		self.authenticate()

	def __getattr__(self, name):
		def method(**kwargs):
			""" Handles undefined methods """

			# Strip out data and params
			data = kwargs.get("data", None)
			params = kwargs.get("params", None)

			# Load API Paths from JSON
			json_data = json.load(open('api_paths.json'))
	
			try:
				api_method = json_data[name]

				verb = api_method['verb']
				path = api_method['path']

				# Replace args, if any are present
				for key in kwargs:
					path = path.replace('{{{}}}'.format(key), str(kwargs[key]))

				# Check to see if there are any unmatched arguments in the path string.
				# If there are, respond with a failure message.
				arg_pattern = "(\{.*?\})"
				arg_matches = re.findall(arg_pattern, path)

				message = ""
				if arg_matches:
					matches_string = (', '.join(arg_matches))
					message = "Error: Unmatched parameter(s) in {}: {}".format(name, matches_string)
					return ResponseObject(message=message)

				action_response = self.perform_action(verb, path, data, params)

				return action_response

			except KeyError:
				return ResponseObject(success = False, message = "API Method {} does not exist".format(name))
			
		return method

	def clean_endpoint(self, endpoint):
		return endpoint.lstrip('//')

	def authenticate(self):
		credentials = self.hash_credentials(self.username, self.password)

		service = OAuth1Service (
			consumer_key = self.consumerKey,
			consumer_secret = self.consumerSecret,
			request_token_url = "%sv1/PortalUser/AccessToken" % self.url
		)

		tokens = service.get_raw_request_token(data = credentials)
		tokens_content = urllib.parse.parse_qs(tokens.content)

		oauth_token = tokens_content[b'oauth_token'][0].decode()
		oauth_tokensecret = tokens_content[b'oauth_token_secret'][0].decode()

		session = OAuth1Session (
			self.consumerKey,
			self.consumerSecret,
			oauth_token,
			oauth_tokensecret
		)

		self.session = session

	def patch_send(self):
	    old_send= http.client.HTTPConnection.send
	    def new_send( self, data ):
	        print(data)
	        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
	    http.client.HTTPConnection.send= new_send

	def get(self, endpoint, debug = False, **kwargs):
		if debug:		
			self.patch_send()
			
		request_url = "%s%s" % (self.url, self.clean_endpoint(endpoint))

		return self.session.get(request_url, header_auth=True, headers={"Accept": "application/json"}, **kwargs)

	def post(self, endpoint, debug = False, **kwargs):
		if debug:		
			self.patch_send()

		request_url = "%s%s" % (self.url, self.clean_endpoint(endpoint))

		return self.session.post(request_url, header_auth=False, headers={"Accept": "application/json", "Content-type": "application/json"}, **kwargs)

	def perform_action(self, verb, path, data, params):
		keywords = {}

		if data:
			keywords['data'] = data
			
		if params:
			keywords['params'] = params

		if verb.lower() == "get":
			action_response = self.get(path, **keywords)

			if action_response.status_code in (200, 201):
				model = json.loads(action_response.text, object_pairs_hook=collections.OrderedDict)

				return ResponseObject(success = True, result = action_response, model = model)
			else:
				return ResponseObject(success = False, result = action_response)

		return ResponseObject(message = "Failed to perform action")


# Load configuration file
config_path = os.path.realpath("../config.yml")
stream = open(config_path, 'r')
config = yaml.load(stream)

auth_settings = config['authentication']['staging']

c = F1Session(
	consumerKey = auth_settings['key'],
	consumerSecret = auth_settings['secret'],
	username = auth_settings['username'],
	password = auth_settings['password'],
	url = auth_settings['url']
	)

# x = c.households_show(id=25117384)

search_parameters = {}
search_parameters['searchFor'] = '{} {}'.format("Erick", "Pece").strip()

x = c.people_search(params=search_parameters)

print(x.model)