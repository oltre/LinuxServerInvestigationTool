env_path       = '/var/www/html/symfony/.env'
env_file       = open(env_path, 'r')
env_content = env_file.read()
for env_line in env_content.split("\n"):
	if env_line.startswith('DATABASE_URL'):
		env_line = env_line.replace("\"", "")

		env_line_list = env_line.split("=")
		database_url = env_line_list[1]
		print database_url

		# TODO : database url parser 


env_file.close()


