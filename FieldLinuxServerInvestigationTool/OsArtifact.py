
import common
import subprocess
import os

class OsArtifactClass():
    def __init__():
		self.history_path_list = []
		self.history_analyze_result = []

		self.install_server_dict = {}
	
		self.os_release = {}
		
		self.netstat = {}
		self.netstat_list = []

		self.process_list = []

	def os_artifact_analyze(self):
		self.osinfo_analyze()
		self.history_analyze()
		self.netstat_analyze()
		self.process_analyze()
		return 1

	def os_artifact_filewrite(self, result_path = './'):
		os_artifact_path = os.path.join(result_path, 'os_artifact')
		os.makedirs(os_artifact_path, exist_ok = True)

		os_release_path = os.path.join(os_artifact_path, 'os_release.json')
		with open(os_release_path, 'w') as fp:
			json.dump(self.os_release, fp, indent = 4)

		history_path = os.path.join(os_artifact_path, 'history')
		with open(history_path, 'w') as fp:
			for history in self.history_analyze_result:
				fp.write("%s\n" % history)

		netstat_path = os.path.join(os_artifact_path, 'netstat.json')
		with open(netstat_path, 'w') as fp:
			json.dump(self.netstat, fp, indent = 4)

		process_path = os.path.join(os_artifact_path, 'process')
		with open(process_path, 'w') as fp:
			for process in self.process_list:
				fp.write("%s\n" % processy)


	def find_history_file(self, name):
		if 'bash' in name:
			self.history_path_list.extend(find_file_list('.bash_history', './'))
		elif 'csh' in name:
			self.history_path_list.extend(find_file_list('.csh_history', './'))
		elif 'ksh' in name:
			self.history_path_list.extend(find_file_list('.ksh_history', './'))
		elif 'tcs' in name:
			self.history_path_list.extend(find_file_list('.tcs_history', './'))

	def history_analyze(self):
		if len(self.history_path_list) == 0:
			self.find_history_file('bash')
			self.find_history_file('csh')
			self.find_history_file('ksh')
			self.find_history_file('tcs')

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
						self.history_analyze_result.append(read_line)

		return 1


	def osinfo_analyze(self):
		# file read
		with open("/etc/os-release") as osrelease:
			for read_line in osrelease:
				try:
					k, v = read_line.rstrip().split("=")
					if v.startswith('"'):
						v = v.strip('"')
					self.os_release[k] = v
				except:
					continue

		# centos additional analysis
		if os_release["NAME"].startswith("CentOS"):
			with open("/etc/centos-release") as centosrelease:
				for read_line in centosrelease:
					read_line = read_line.strip('\n')
					self.os_release["CENTOS_DETAIL"] = read_line

		# os installation time analysis
		# output after time value conversion
		ctime = 0
		if self.os_release["NAME"].startswith("CentOS"):
			ctime = os.path.getctime("/root/anaconda-ks.cfg")
		else:
			ctime = os.path.getctime("/var/log/installer/syslog")

		install_time = datetime.datetime.fromtimestamp(ctime)
		self.os_release["INSTALL_DATETIME"] = install_time.strftime("%Y-%m-%d %H:%M:%S")

		return 1


	def netstat_analyze(self):
		netstatcmd = subprocess.Popen(['netstat', '-apt'], stdout = subprocess.PIPE)
		netstat = netstatcmd.communicate()[0].decode()
	
		self.netstat_list = netstat.split("\n")
		del(netstat_list[0:2])
		for netstat_line in netstat_list:
			netstat_line_list = netstat_line.split()

			if len(netstat_line_list) == 7 and netstat_line_list[0] in 'tcp' and netstat_line_list[5] in 'ESTABLISHED':
				if netstat_line_list[6] in ('mysql', 'mariadb', 'mongodb', 'oracle'):
					self.netstat["SRC_ADDR"] = netstat_line_list[3]
					self.netstat["DST_ADDR"] = netstat_line_list[4]
					self.netstat["NAME"] = netstat_line_list[6]

		return 1

	def process_analyze(self):
		pscmd = subprocess.Popen(['ps', 'aux'], stdout = subprocess.PIPE)
		ps = pscmd.communicate()[0].decode()

		self.processes = ps.split("\n")
		for pscmd_line in self.processes:
			if 'mysql' in pscmd_line.lower():
				self.install_server_dict["DATABASE_SERVER"] = "MYSQL"
			elif 'mariadb' in pscmd_line.lower():
				self.install_server_dict["DATABASE_SERVER"] = "MARIADB"
			elif 'oracle' in pscmd_line.lower():
				self.install_server_dict["DATABASE_SERVER"] = "ORACLE"
			elif 'mongodb' in pscmd_line.lower():
				self.install_server_dict["DATABASE_SERVER"] = "MONGODB"
			elif 'httpd' in pscmd_line.lower():
				self.install_server_dict["WEB_SERVER"] = "APACHE"
			elif 'nginx' in pscmd_line.lower():
				self.install_server_dict["WEB_SERVER"] = "NGINX"

		return 1






