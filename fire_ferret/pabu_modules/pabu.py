from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from os.path import basename
import pabu_modules.aass as aass
import pabu_modules.logger as log
import re, errno, urllib.request, os, requests, shutil

# function to specifically download the index file
def download_index(url, site_directory, mobile_device):
	site_directory = re.sub(r'\/$', '', site_directory)
	link_file_path = site_directory + '/index.html'

	create_directory(site_directory)
	download_from_url(url, link_file_path, mobile_device)
	return True

def download_asset(asset_url, file_path, mobile_device):
	download_from_url(asset_url, file_path, mobile_device)

# function to download a single file and save it to a specified fiepath
def download_from_url(url, file_path, mobile_device):
	log.log("Downloading URL | \"" + url + "\"", "url_download_attempt")
	if mobile_device == "false":
		ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
	else:
		ua = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'
	# set user agent to prevent 403 errors
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', ua)]
	urllib.request.install_opener(opener)
	# try and download asset
	try:
		urllib.request.urlretrieve(url, file_path)
	# raise errors
	except urllib.error.HTTPError as e:
		if e.code == 404:
			log.log("404 Error - File not found | \"" + url + "\"", "error")
			return False
		elif e.code == 500:
			log.log("500 Error - Internal Server Error | \"" + url + "\"", "error")
			return False
		else:
			raise e
	except urllib.error.URLError as eUrl:
		log.log("URL Error -  | \"" + url + "\"", "URL-Error")
		return False
	except Exception as ex:
		raise ex
		
	return True

def determine_file_path(asset_url, site_directory):
	folder = site_directory + aass.determine_storage_location(asset_url)
	filename = urlsplit(asset_url).path
	file_path = folder + '\\' + basename(filename)
	create_directory(folder)
	return file_path

# function to create a directory
def create_directory(directory):
	# try and make new directory
	try:
		os.makedirs(directory)
	# raise error if error not errno.EExist
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	return True

def find_assets(file_path):
	# parse the HTML with BeautifulSoup package
	data = open(file_path, 'r', encoding="utf8")
	print ("Making soup")
	soup = BeautifulSoup(data, "html.parser")

	# store all link tags in variable
	print ("Getting the ingredients")
	asset_tags = soup.find_all("link")

	# loop through all script tags and push to asset_tags variable (array)
	for a in soup.find_all("script"):
		asset_tags.append(a)

	# loop through all img tags and push to asset_tags variable (array)
	for a in soup.find_all("img"):
		asset_tags.append(a)

	# loop through all div tags and push to asset_tags variable (array)
	for a in soup.find_all("div"):
		asset_tags.append(a)

	# loop through all source tags and push to asset_tags variable (array)
	for a in soup.find_all("source"):
		asset_tags.append(a)

	return asset_tags

def find_asset_urls(asset_tags):
	# empyt array to store downloaded asset hrefs, this is checked to ensure assets are not downloaded more than once
	downloaded_assets = []
	asset_urls = []
	# loop through all stored tags in asset_tags variable
	for asset in asset_tags:
		# loop through attributes and match regex for any known and desired filetype 
		for attr in asset.attrs:
			# set href variable to false because setting it in the else statement caused errors
			href = False
			# store attribute value in variable
			val = str(asset.get(attr))
			# check if attribute value contains known, desirable file extensions (using regex)
			if re.search(r"\.(ico|png|webP|jpg|jpeg|gif|bmp|js|css|scss|sass|woff|svg|json|pdf|txt)", val):
				href = val
				log.log('Found Asset | [' + attr + '] = ' + href, 'found_assets')
			# if href not equal to false
			if href != False:
				# strip all unneccesary chars from href
				old_ref = href
				href = aass.purify_url_string(href)
				log.log('Confirmed Asset Purified | [' + old_ref + '] = ' + href, 'confirmed_assets--purified')
				# add href to downloaded_assets
				asset_urls.append(href)


	return asset_urls

def build_url(asset_url, base_url):
	log.log("Received Asset URL | \"" + asset_url + "\"", "asset_url_builder")
	if re.search(r"^\/\/", asset_url): 
		return 'https:' + asset_url
	elif re.search(r"^\/", asset_url): 
		return base_url + re.sub(r"^\/", '', asset_url)
	elif re.search(r"^http", asset_url):
		return asset_url
	elif re.search(r"\.\.\/", asset_url):
		return base_url + re.sub(r"\.\.\/", '', asset_url)
	elif re.search(r"^[a-z]", asset_url) and asset_url[0:3] != "http":
		return base_url + re.sub(r"^\/", '', asset_url)
	else:
		return "https://"+asset_url

def grab_images_from_css(filepath):
	css_asset_links = []
	file = open(filepath, "r", encoding="utf8")
	images = re.findall('url\(([^)]+)\)', file.read())
	file.close()
	for link in images:
		if len(re.findall(";base64,", link)) == 0 and link not in css_asset_links:
			pure_link = aass.purify_url_string(link)
			css_asset_links.append(pure_link)

	return css_asset_links

def update_link(old_link, new_link, site_directory, file):
	# log message to console
	new_link = new_link.replace('\\', '/')
	site_directory = site_directory.replace('\\', '/')
	log.log("Saving Asset | \"" + old_link + "\" [as] \"" + new_link + "\"", "asset_storage")
	if site_directory[-1:] == "/":
		site_directory = site_directory[:-1]

	# try opening file with read permissions
	try:
		index = open(file, 'r', encoding="utf8")
	# raise errors
	except Exception as e:
		raise e
	# store file content and replace original asset link with local equivalent
	new_content = index.read().replace(old_link, new_link)
	new_content = new_content.replace(site_directory, '')
	# close index file
	index.close()
	# reopen with write permissions
	index = open(file, 'w', encoding="utf8")
	# replace file content with new version
	index.write(new_content)
	# close file
	index.close()
	return True

# function to generate dev enviroment from template folder
def generate_dev_enviroment(config):
	# set variables based on config file
	client_directory = config["client_directory"]
	test_id = config["test_id"]
	test_directory = client_directory + test_id
	site_directory = test_directory + '/site'
	code_template = config["enviroment_template"]
	link_file_path = site_directory + '/index.html'

	# try opening file with read permissions
	try:
		index = open(link_file_path, 'r', encoding="utf8")
	# raise errors
	except Exception as e:
		raise e
	# store file content and replace original asset link with local equivalent
	new_content = index.read().replace('</body>','<script type="text/javascript" src="/locro/locro.js" />\n</body>')
	# close index file
	index.close()
	# reopen with write permissions
	index = open(link_file_path, 'w', encoding="utf8")
	# replace file content with new version
	index.write(new_content)
	# close file
	index.close()
	
	# try copying locro js modules to local site locro folder
	try:
		shutil.copytree('.\\Code_Templates\\locro_js_module', site_directory + '/locro')
	# raise error
	except Exception as e:
		raise e

	# try copying gulp and package to local site folder
	try:
		shutil.copy('.\\Code_Templates\\localhost\\package.json', site_directory)
		# shutil.copy('.\\Code_Templates\\localhost\\gulpfile.js', site_directory)
	# raise error
	except Exception as e:
		raise e

	if os.path.isdir(test_directory + '/code') != True:
		print ("importing code template")
		shutil.copytree(code_template, test_directory + '/code')