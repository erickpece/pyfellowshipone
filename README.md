# pyfellowshipone: Python Fellowship One API Library

pyfellowshipone is a planned library for making requests to the Fellowship One API.

This library currently only supports 2nd party credential-based authentication.

## Usage:

### Search for a person

```
from f1api import F1API

api = F1API (
	consumerKey = "your_key",
	consumerSecret = "your_secret",
	username = "your_username",
	password = "your_password",
	url = "your_url"
	)

search_parameters = {}
search_parameters['searchFor'] = '{} {}'.format("John", "Doe").strip()

result = api.people_search(params=search_parameters)

print(result.model)
```

## Credits:

API Paths concept borrowed from the excellent PHP library at https://github.com/deboorn/FellowshipOne-API