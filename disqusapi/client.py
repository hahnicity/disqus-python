import httplib
import os.path
import simplejson
import urllib
import warnings

import disqusapi
from disqusapi.exception import APIError, ERROR_MAP, InterfaceNotDefined
from disqusapi.result import Result


HOST = 'disqus.com'
INTERFACES = simplejson.loads(
    open(os.path.join(os.path.dirname(__file__), 'interfaces.json'), 'r').read()
)


class Resource(object):
    def __init__(self, api, interface=INTERFACES, node=None, tree=()):
        self.api = api
        self.node = node
        self.interface = interface
        if node:
            tree = tree + (node,)
        self.tree = tree

    def __getattr__(self, attr):
        if attr in getattr(self, '__dict__'):
            return getattr(self, attr)
        interface = self.interface
        if attr not in interface:
            interface[attr] = {}
        return Resource(self.api, interface[attr], attr, self.tree)

    def __call__(self, **kwargs):
        return self._request(**kwargs)

    def _request(self, **kwargs):
        # Handle undefined interfaces
        resource = self.interface
        for k in resource.get('required', []):
            if k not in (x.split(':')[0] for x in kwargs.iterkeys()):
                raise ValueError('Missing required argument: %s' % k)

        method = kwargs.pop('method', resource.get('method'))

        if not method:
            raise InterfaceNotDefined()

        api = self.api

        version = kwargs.pop('version', api.version)
        format = kwargs.pop('format', api.format)

        conn = httplib.HTTPSConnection(HOST)

        path = '/api/%s/%s.%s' % (version, '/'.join(self.tree), format)

        if 'api_secret' not in kwargs and api.secret_key:
            kwargs['api_secret'] = api.secret_key
        if 'api_public' not in kwargs and api.public_key:
            kwargs['api_key'] = api.public_key

        # We need to ensure this is a list so that
        # multiple values for a key work
        params = []
        for k, v in kwargs.iteritems():
            if isinstance(v, (list, tuple)):
                for val in v:
                    params.append((k, val))
            else:
                params.append((k, v))

        headers = {
            'User-Agent': 'disqus-python/%s' % disqusapi.__version__
        }

        if method == 'GET':
            path = '%s?%s' % (path, urllib.urlencode(params))
            data = ''
        else:
            data = urllib.urlencode(params)

        conn.request(method, path, data, headers)

        response = conn.getresponse()
        # Let's coerce it to Python
        data = api.formats[format](response.read())

        if response.status != 200:
            raise ERROR_MAP.get(data['code'], APIError)(data['code'], data['response'])

        if isinstance(data['response'], list):
            return Result(data['response'], data.get('cursor'))
        return data['response']


class DisqusAPI(Resource):
    formats = {'json': lambda x: simplejson.loads(x)}

    def __init__(self,
                 secret_key=None,
                 public_key=None,
                 format='json',
                 version='3.0',
                 **kwargs):
        self.secret_key = secret_key
        self.public_key = public_key
        if not public_key:
            warnings.warn('You should pass ``public_key`` in addition to your secret key.')
        self.format = format
        self.version = version
        super(DisqusAPI, self).__init__(self)

    def _request(self, **kwargs):
        raise SyntaxError('You cannot call the API without a resource.')

    def _get_key(self):
        return self.secret_key
    key = property(_get_key)

    def setSecretKey(self, key):
        self.secret_key = key
    setKey = setSecretKey

    def setPublicKey(self, key):
        self.public_key = key

    def setFormat(self, format):
        self.format = format

    def setVersion(self, version):
        self.version = version
