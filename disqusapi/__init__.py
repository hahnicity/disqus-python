"""
disqus-python
~~~~~~~~~~~~~

disqus = DisqusAPI(api_secret=secret_key)
disqus.trends.listThreads()
"""
from disqusapi.client import DisqusAPI
from disqusapi.paginator import Paginator

try:
    __version__ = __import__('pkg_resources').get_distribution('disqusapi').version
except:
    __version__ = 'unknown'


__all__ = ['DisqusAPI', 'Paginator']
