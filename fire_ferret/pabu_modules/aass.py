import pabu_modules.logger as log
import re

# determine asset_type based off last 3 characters of a string, uses purify_url_string function.
def determine_asset_type(asset_url):
	cleansed_string = purify_url_string(asset_url)
	asset_type = cleansed_string[-3:].replace('.','')
	return asset_type

# remove query parameters and hashtags from URL string.
def purify_url_string(url_string):
	url_string = re.sub(r"^ ", '', url_string)
	pure_string = re.sub(r"((^\/\/)|((\?|\#| ).*)|url|\(|background-image:|\)|\"|\'|;)", '', url_string).strip()
	log.log('Link Purification | ' + url_string + ' becomes ' + pure_string , 'purified_links')
	return pure_string

def determine_storage_location(asset_url):
	asset_type = determine_asset_type(asset_url)
	asset_directory = "\\" + asset_type
	return asset_directory