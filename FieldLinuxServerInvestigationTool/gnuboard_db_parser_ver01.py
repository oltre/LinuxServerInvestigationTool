import os
import re
import json

def remove_define(line):
	line = line.replace('define', '')
	line = line.replace('(', '')
	line = line.replace(')', '')
	line = line.replace("'", '')
	line = line.replace(";", '')
	return line

document_root = '/var/www/html/gnuboard'

database_connect_info = {}
config_path = os.path.join(document_root, 'config.php')
with open(config_path, 'r') as config:
	for config_line in config:
		if re.search(r'define\(\s*\'G5_DB', config_line):
			if re.search(r'G5_DBCONFIG_FILE', config_line):
				db_config_path = os.path.join(document_root, 'data', 'dbconfig.php')
				with open(db_config_path) as db_config:
					for db_config_line in db_config:
						if re.search(r'define\(\s*\'G5_', db_config_line):
							db_config_line = remove_define(db_config_line)
							#print(db_config_line)
							k, v = db_config_line.split(',')
							if "db" in k.lower():
								database_connect_info["DATABASE"] = v.strip()
							elif "user" in k.lower():
								database_connect_info["USER"] = v.strip()
							elif "password" in k.lower():
								database_connect_info["PASSWORD"] = v.strip()
							elif "host" in k.lower():
								database_connect_info["HOST"] = v.strip()

web_framework_path = os.path.join('./', 'web_framework')
os.makedirs(web_framework_path, exist_ok = True)

result_path = os.path.join(web_framework_path, 'gnuboard.json')
with open(result_path, 'w') as result:
	json.dump(web_framework_path, result, indent = 4)
