# netstat parser

# backup
#shutil.copy2("/etc/os-release", "./os-release")

# calc hash value(MD5, SHA1)

# parsing
import subprocess
import os
import json

# file read & dictionary style
def get_netstat():
	netstatcmd = subprocess.Popen(['netstat', '-apt'], stdout = subprocess.PIPE)
	netstat = netstatcmd.communicate()[0].decode()
	
	netstat_list = netstat.split("\n")
	del(netstat_list[0:2])
	netstat = {}
	for netstat_line in netstat_list:
		netstat_line_list = netstat_line.split()

		if len(netstat_line_list) == 7 and netstat_line_list[0] in 'tcp' and netstat_line_list[5] in 'ESTABLISHED':
			if netstat_line_list[6] in ('mysql', 'mariadb', 'mongodb', 'oracle'):
				netstat["SRC_ADDR"] = netstat_line_list[3]
				netstat["DST_ADDR"] = netstat_line_list[4]
				netstat["NAME"] = netstat_line_list[6]

	return netstat

netstat_dict = get_netstat()

os_artifact_path = os.path.join('./', 'os_artifact')
os.makedirs(os_artifact_path, exist_ok = True)

netstat_path = os.path.join(os_artifact_path, 'netstat.json')
with open(netstat_path, 'w') as netstat_result:
	json.dump(netstat_dict, netstat_result, indent = 4)

