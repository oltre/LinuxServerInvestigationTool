import re
import json

db_config_path = '/var/www/html/laravel/config/database.php'
env_path       = '/var/www/html/laravel/.env'

db_config_file = open(db_config_path, 'r')
env_file       = open(env_path, 'r')

db_config_content = db_config_file.read()
env_content = env_file.read()

db_config_dictionary = {}
env_dictionary = {}
for env_line in env_content.split("\n"):
	if env_line is not '':
		(key, val) = env_line.split('=', 1)
		env_dictionary[key] = val

db_config_file.close()
env_file.close()

for x in re.findall(r'("[^\n]*"(?!\\))|(//[^\n]*$|/(?!\\)\*[\s\S]*?\*(?!\\)/)',db_config_content,8):
	db_config_content = db_config_content.replace(x[1],'')

db_config_content_list = db_config_content.split("\n")
for db_config_line in db_config_content_list:
	if db_config_line.find('extension_loaded') > 0:
		continue
	if re.search(r'^\'.*\'\=\>((env)|(\'))', db_config_line.strip().replace(' ', '')):
		


	

