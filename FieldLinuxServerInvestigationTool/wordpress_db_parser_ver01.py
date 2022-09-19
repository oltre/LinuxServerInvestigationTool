import re

db_config_path = '/var/www/html/wordpress/wp-config.php'

db_config_file = open(db_config_path, 'r')

db_config_content = db_config_file.read()

for db_config_line in db_config_content.split("\n"):
	if re.search(r'define\(\s*\'(DB)|(db)|(Db)|(dB)', db_config_line):
		print(db_config_line)

		# TODO : define ( ) remove 
	

