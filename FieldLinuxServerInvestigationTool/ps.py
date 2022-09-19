# ps parser

# backup
#shutil.copy2("/etc/os-release", "./os-release")

# calc hash value(MD5, SHA1)

# parsing
import subprocess
import os
import json

# file read & dictionary style
def get_processes():
	pscmd = subprocess.Popen(['ps', 'aux'], stdout = subprocess.PIPE)
	ps = pscmd.communicate()[0].decode()

	processes = ps.split("\n")
	running_process = {}
	for pscmd_line in processes:
		if 'mysql' in pscmd_line.lower():
			running_process["DATABASE_SERVER"] = "MYSQL"
		elif 'mariadb' in pscmd_line.lower():
			running_process["DATABASE_SERVER"] = "MARIADB"
		elif 'oracle' in pscmd_line.lower():
			running_process["DATABASE_SERVER"] = "ORACLE"
		elif 'mongodb' in pscmd_line.lower():
			running_process["DATABASE_SERVER"] = "MONGODB"
		elif 'httpd' in pscmd_line.lower():
			running_process["WEB_SERVER"] = "APACHE"
		elif 'nginx' in pscmd_line.lower():
			running_process["WEB_SERVER"] = "NGINX"

	return running_process

running_process = get_processes()

os_artifact_path = os.path.join('./', 'os_artifact')
os.makedirs(os_artifact_path, exist_ok = True)

process_path = os.path.join(os_artifact_path, 'run_process.json')
with open(process_path, 'w') as run_proc_result:
	json.dump(running_process, run_proc_result, indent = 4)


