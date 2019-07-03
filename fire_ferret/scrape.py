# import relevant packages for use in this script
from pathlib import Path
import pabu_modules.pabu as pabu
import pabu_modules.aass as aass
import pabu_modules.logger as log
import pabu_modules.url_handler as urlh
import json

# set config file path
config_file = Path("config.json")
# check if config file exists
if config_file.is_file():
	# success message
	print ("Config file exists")

	# open config file
	with open('config.json', 'r') as f:
		# relevant messaging
		print ("Checking config file")
		# set variables based on config settings
		config = json.load(f)
		webpage_url = config['url']
		client_directory = config["client_directory"]
		test_id = config["test_id"]
		mobile_device = config["mobile_device"]
		test_directory = client_directory + test_id
		site_directory = test_directory + '\\site'
		code_directory = test_directory + '\\code'

		if webpage_url[-1:] != "/":
			webpage_url += "/"

		# pass the requested url data over to the scrape and save function in the pabu package
		print ("Saving the recipe")
		pabu.download_index(webpage_url, site_directory, mobile_device)

		root_url = urlh.determine_root_url(webpage_url)

		asset_tags = pabu.find_assets(site_directory + '\\index.html')
		asset_urls = pabu.find_asset_urls(asset_tags)

		# loop through all stored tags in asset_tags variable
		for asset in asset_urls:
			asset = asset.strip()
			if asset[0:1] != '//' and (asset[0] == '/' or asset[0] == '.'):
				complete_asset_url = pabu.build_url(asset, root_url)
				local_asset_file_path = pabu.determine_file_path(complete_asset_url, site_directory)
				pabu.download_asset(complete_asset_url, local_asset_file_path, mobile_device)
				pabu.update_link(asset, local_asset_file_path, site_directory, site_directory+'/index.html')

				asset_type = aass.determine_asset_type(complete_asset_url)

				if asset_type == 'css':
					css_asset_links = pabu.grab_images_from_css(local_asset_file_path)
					for css_asset in css_asset_links:
						if css_asset[0:1] != '//' and (css_asset[0] == '/' or css_asset[0] == '.'):
							css_asset_url = pabu.build_url(css_asset, root_url)
							local_css_asset_file_path = pabu.determine_file_path(css_asset_url, site_directory)
							# log.log("\"" + css_asset + "\" -> \"" + css_asset_url + "\" in " + asset, "CSS Asset URL")
							pabu.download_asset(css_asset_url, local_css_asset_file_path, mobile_device)
							pabu.update_link(css_asset, local_css_asset_file_path, site_directory, local_asset_file_path)
					
		# Once done pass config file onto generae_dev_enviroment (function found in pabu file)
		pabu.generate_dev_enviroment(config)