import re
import json
import ast

db_config_path = '/var/www/html/laravel/config/database.php'
env_path       = '/var/www/html/laravel/.env'

db_config_file = open(db_config_path, 'r')
env_file       = open(env_path, 'r')

db_config_content = db_config_file.read()
env_content = env_file.read()

env_dictionary = {}
# .env file to dictionary
for env_line in env_content.split("\n"):
	if env_line != '':
		(key, val) = env_line.split('=', 1)
		env_dictionary[key] = val

db_config_file.close()
env_file.close()

db_config_content_list = db_config_content.split("\n")

key_stack = []
value_stack = []
for db_config_line in db_config_content_list:
	key = ''
	value = ''

	# searching : 'test' => 'ttt', 'test' => true, 'test' => false, 'test' => null
	if re.search(r'\'.*\'=>((\'.*\')|(true)|(flase)|(null))\,', db_config_line.replace(" ", "")):
		#print ("search #1" + db_config_line)
		line_list = db_config_line.replace("'", "").replace(" ", "").split("=>")
		key = line_list[0]
		value = line_list[1].replace(",", "")
	
	# searching : 'test' => [
	elif re.search(r'\'.*\'=>\[', db_config_line.replace(" ", "")):
		#print("search #2" + db_config_line)
		key = db_config_line.replace("'", "").replace(" ", "").split("=>")[0]
		value = '['

	# searching : 'test' => env('test', 'test'),
	elif re.search(r'\'.*\'=>env\(\'.*\'\,.*\),', db_config_line.replace(" ", "")):
		#print("search #3" + db_config_line)
		line_list = db_config_line.replace("'", "").replace(" ", "").replace(")", "").split("=>")
		key = line_list[0]
		value = env_dictionary.get(key)
		if value is None:
			value_list = line_list[1].split(',')
			value = value_list[1]
	
	# searching : 'test' => env('test'),
	elif re.search(r'\'.*\'=>env\(\'.*\'\),', db_config_line.replace(" ", "")):
		#print("search #4" + db_config_line)
		key = db_config_line.replace("'", "").replace(" ", "").split("=>")[0]
		value = env_dictionary.get(key)
	else:
		continue

	key_stack.append(key)
	value_stack.append(value)
	if value is None:
		print(key + ", ")
	else:
		print(key + ", " + value)

# TODO : make dictionary

