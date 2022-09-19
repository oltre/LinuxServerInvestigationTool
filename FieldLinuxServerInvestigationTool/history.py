# history

import os
import common 

class HistoryParser():
	def __init__():
		self.history_path_list = []
		self.history_result_path = ''
		self.install_server_dict = {}

	def find_history_file(self, name):
		if 'bash' in name:
			self.history_path_list.extend(find_file_list('.bash_history', './'))
		elif 'csh' in name:
			self.history_path_list.extend(find_file_list('.csh_history', './'))
		elif 'ksh' in name:
			self.history_path_list.extend(find_file_list('.ksh_history', './'))
		elif 'tcs' in name:
			self.history_path_list.extend(find_file_list('.tcs_history', './'))

	def history_analyze(self, system_info_path = './os_artifact'):
		if len(self.history_path_list) == 0:
			self.find_history_file('bash')
			self.find_history_file('csh')
			self.find_history_file('ksh')
			self.find_history_file('tcs')

		history_result_path = os.path.join(system_info_path, 'history_list')
		with open(history_result_path, 'w') as history_result:
			for history_path in self.history_path_list:
				with open(history_path, 'r') as history:
					for read_line in history:
						found = False
						lower_line = read_line.casefold()
						if 'mysql' in lower_line and ('install' in lower_line or '-p' in lower_line or 'wget' in lower_line):
							self.install_server_dict["DATABASE_SERVER"] = "MYSQL"
							found = True
						elif 'mariadb' in lower_line and ('install' in lower_line or '-p' in lower_line or 'wget' in lower_line):
							self.install_server_dict["DATABASE_SERVER"] = "MARIADB"
							found = True
						elif 'oracle' in lower_line and ('install' in lower_line or 'wget' in lower_line):
							self.install_server_dict["DATABASE_SERVER"] = "ORACLE"
							found = True
						elif 'mongodb' in lower_line and ('install' in lower_line or 'wget' in lower_line):
							self.install_server_dict["DATABASE_SERVER"] = "MONGODB"
							found = True
						elif 'apache' in lower_line and ('install' in lower_line or 'systemctl' in lower_line or 'wget' in lower_line):
							self.install_server_dict["WEB_SERVER"] = "APACHE"
							found = True
						elif 'nginx' in lower_line and ('install' in lower_line or 'systemctl' in lower_line or 'wget' in lower_line or 'configure' in lower_line):
							self.install_server_dict["WEB_SERVER"] = "NGINX"
							found = True
						elif 'codeigniter' in lower_line and ('wget' in lower_line or 'create' in lower_line):
							self.install_server_dict["WEB_FRAMEWORK"] = "CODEIGNITER"
							found = True
						elif 'symfony' in lower_line and ('wget' in lower_line or 'create' in lower_line):
							self.install_server_dict["WEB_FRAMEWORK"] = "SYMFONY"
							found = True
						elif 'laravel' in lower_line and ('wget' in lower_line or 'create' in lower_line):
							self.install_server_dict["WEB_FRAMEWORK"] = "LARAVEL"
							found = True
						elif 'wordpress' in lower_line and ('wget' in lower_line or 'create' in lower_line):
							self.install_server_dict["WEB_FRAMEWORK"] = "WORDPRESS"
							found = True
						elif 'gnuboard' in lower_line and 'wget' in lower_line:
							self.install_server_dict["WEB_FRAMEWORK"] = "GNUBOARD"
							found = True

						if found:
							history_result.write(read_line)

		return self.install_server_dict