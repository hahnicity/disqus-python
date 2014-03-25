#disqus-python

## Installation
Let's start with installing the API:

	pip install disqus-python

## Usage
### Getting Started
Use the API by instantiating it, and then calling the method through dotted notation chaining::

	from disqusapi import DisqusAPI

	disqus = DisqusAPI(secret_key=<secret key>, public_key=<public key>)
	for result in disqus.trends.listThreads():
	    print result

Parameters (including the ability to override version, api_secret, and format) are passed as keyword arguments to the resource call::

	disqus.posts.details(post=1, version='3.0')

### Pagination
Paginating through endpoints is easy as well::

	from disqusapi import Paginator

	paginator = Paginator(disqus.trends.listThreads, forum='disqus')
	for result in paginator:
	    print result

	# pull in a maximum of 500 results (this limit param differs from the endpoint's limit param)
	for result in paginator(limit=500):
	    print result

### Accessing APIs with Authentication
Some of the disqus APIs require an access token. This client can use an access token 
obtained from OAuth2 or our application's actual access token.

	from disqusapi import DisqusAPI

	disqus = DisqusAPI(secret_key=<secret key>, public_key=<public key>)
	for result in disqus.applications.listUsage(access_token=<Access token>):
	    print result

### More methods
Documentation on all methods, as well as general API usage can be found at http://disqus.com/api/

Currently supported methods through the DisqusAPI class are all defined there. For 
example if we have an API under `Posts` named `restore` then our API call through the
`DisqusAPI` would look like

    response = disqus.posts.restore(posts=[1, 2, 3])

We are attempting to restore posts with ids 1, 2, and 3 here and `DisqusAPI` will take 
care of the hard work for us
