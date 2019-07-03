import pabu_modules.logger as log
from urllib.parse import urlparse

def determine_root_url(url_str):
	parsed_uri = urlparse(url_str)
	root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	log.log("Root URL | \"" + root_url + "\"", "root_url")
	return root_url