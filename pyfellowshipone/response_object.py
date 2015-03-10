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