import os
def log(error, type):
	print(error)
	do_the_log(error, type)
	do_the_log(error, 'global_log')

def do_the_log(error, type):
	if os.path.isdir("./logs/") != True:
		os.makedirs("./logs/")
	error_log_file_path = "./logs/"+type+"_log.txt"
	error_log_file = open(error_log_file_path, "a+")
	error_log_file.write(error + '\n')
	error_log_file.close()