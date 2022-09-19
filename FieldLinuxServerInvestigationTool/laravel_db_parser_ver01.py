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
for env_line in env_content.split("\n"):
	if env_line is not '':
		(key, val) = env_line.split('=', 1)
		env_dictionary[key] = val

db_config_file.close()
env_file.close()

db_config_content_list = db_config_content.split("\n")
env_content_list = env_content.split("\n")

new_db_config = ''

for db_config_line in db_config_content_list:
	if db_config_line.find('extension_loaded') > 0:
		continue
	if re.search(r'^((return)|(\])|(\'.*\'))', db_config_line.strip()):
		new_line = db_config_line
		env_list = re.findall(r'env\(\'.*\'', db_config_line)


		for env in env_list:
			env_data = ''
			for env_key in re.findall(r'\'[a-zA-Z]*_[a-zA-Z]*\'', env):
				env_data = env_dictionary.get(env_key.strip('\''))


			if env_data is not None:
				new_line = re.sub(r'env\(.*\)', '\'' + env_data + '\'', db_config_line)
			else:
				new_line = re.sub(r'env\(.*\)', '\'\'', db_config_line)

		
		new_db_config += new_line

new_db_config = new_db_config.replace("=>", ":")
new_db_config = new_db_config.replace("[", "{")
new_db_config = new_db_config.replace("]", "}")
new_db_config = new_db_config.replace("\'", "\"")
new_db_config = new_db_config.replace("return", "")

db_config_json = json.dumps(new_db_config)
db_config_json_dict = json.loads(db_config_json)
#print(db_config_json_dict)

print type(db_config_json_dict)
db_config_json_dict = ast.literal_eval(db_config_json_dict)
print type(db_config_json_dict)




	

