# operating system check

import os
import datetime
import json

class OsRelease():
	def __init__():
		self.os_release = {}

	def osinfo_analyze():
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







os_artifact_path = os.path.join('./', 'os_artifact')
os.makedirs(os_artifact_path, exist_ok = True)

os_release_path = os.path.join(os_artifact_path, 'os_release.json')
with open(os_release_path, 'w') as os_release_result:
	json.dump(os_release, os_release_result, indent = 4)


