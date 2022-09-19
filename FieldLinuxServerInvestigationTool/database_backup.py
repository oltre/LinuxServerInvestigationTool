
import os
import re
import subprocess
import json
import ast
import datetime
import hashlib

# history file find
def findfile(name, path):
	filepathlist = []
	for dirpath, dirname, filename in os.walk(path):
		if name in filename:
			#print(os.path.join(dirpath, name))
			filepathlist.append(os.path.join(dirpath, name))

	return filepathlist

def remove_define(line):
	line = line.replace('define', '')
	line = line.replace('(', '')
	line = line.replace(')', '')
	line = line.replace("'", '')
	line = line.replace(";", '')
	return line

os_release = {}
install_server_dict = {}

print("=> Operating system analysis")
with open("/etc/os-release") as filehandler:
	for read_line in filehandler:
		try:
			k, v = read_line.rstrip().split("=")
			if v.startswith('"'):
				v = v.strip('"')
			os_release[k] = v
		except:
			continue

# centos additional analysis
if os_release["NAME"].startswith("CentOS"):
	with open("/etc/centos-release") as filehandler:
		for read_line in filehandler:
			read_line = read_line.strip('\n')
			os_release["CENTOS_DETAIL"] = read_line

# os installation time analysis
# output after time value conversion
ctime = 0
if os_release["NAME"].startswith("CentOS"):
	ctime = os.path.getctime("/root/anaconda-ks.cfg")
else:
	ctime = os.path.getctime("/var/log/installer/syslog")

os_release["INSTALL_DATETIME"] = ctime

install_time = datetime.datetime.fromtimestamp(ctime)
os_release["INSTALL_DATETIME"] = install_time.strftime("%Y-%m-%d %H:%M:%S")

os_artifact_path = os.path.join('./', 'os_artifact')
os.makedirs(os_artifact_path, exist_ok = True)

os_release_path = os.path.join(os_artifact_path, 'os_release.json')
with open(os_release_path, 'w') as os_release_result:
	json.dump(os_release, os_release_result, indent = 4)


print("=> history analysis")
history_list = findfile('.bash_history', '/')
history_list.extend(findfile('.csh_history', '/'))
history_list.extend(findfile('.ksh_history', '/'))
history_list.extend(findfile('.tcsh_history', '/'))

# file read & dictionary style
os_artifact_path = os.path.join('./', 'os_artifact')
os.makedirs(os_artifact_path, exist_ok = True)

history_list_path = os.path.join(os_artifact_path, 'history_list')
with open(history_list_path, 'w') as history_list_result:
	for history in history_list:
		with open(history, 'r') as filehandler:
			for read_line in filehandler:
				found = False
				lower_line = read_line.casefold()
				if 'mysql' in lower_line and ('install' in lower_line or '-p' in lower_line or 'wget' in lower_line):
					install_server_dict["DATABASE_SERVER"] = "MYSQL"
					found = True
				elif 'mariadb' in lower_line and ('install' in lower_line or '-p' in lower_line or 'wget' in lower_line):
					install_server_dict["DATABASE_SERVER"] = "MARIADB"
					found = True
				elif 'oracle' in lower_line and ('install' in lower_line or 'wget' in lower_line):
					install_server_dict["DATABASE_SERVER"] = "ORACLE"
					found = True
				elif 'mongodb' in lower_line and ('install' in lower_line or 'wget' in lower_line):
					install_server_dict["DATABASE_SERVER"] = "MONGODB"
					found = True
				elif 'apache' in lower_line and ('install' in lower_line or 'systemctl' in lower_line or 'wget' in lower_line):
					install_server_dict["WEB_SERVER"] = "APACHE"
					found = True
				elif 'nginx' in lower_line and ('install' in lower_line or 'systemctl' in lower_line or 'wget' in lower_line or 'configure' in lower_line):
					install_server_dict["WEB_SERVER"] = "NGINX"
					found = True
				elif 'codeigniter' in lower_line and ('wget' in lower_line or 'create' in lower_line):
					install_server_dict["WEB_FRAMEWORK"] = "CODEIGNITER"
					found = True
				elif 'symfony' in lower_line and ('wget' in lower_line or 'create' in lower_line):
					install_server_dict["WEB_FRAMEWORK"] = "SYMFONY"
					found = True
				elif 'laravel' in lower_line and ('wget' in lower_line or 'create' in lower_line):
					install_server_dict["WEB_FRAMEWORK"] = "LARAVEL"
					found = True
				elif 'wordpress' in lower_line and ('wget' in lower_line or 'create' in lower_line):
					install_server_dict["WEB_FRAMEWORK"] = "WORDPRESS"
					found = True
				elif 'gnuboard' in lower_line and 'wget' in lower_line:
					install_server_dict["WEB_FRAMEWORK"] = "GNUBOARD"
					found = True

				if found:
					history_list_result.write(read_line)

print("=> process list analysis")
def get_processes():
	pscmd = subprocess.Popen(['ps', 'aux'], stdout = subprocess.PIPE)
	ps = pscmd.communicate()[0].decode()

	processes = ps.split("\n")
	running_process = {}
	for pscmd_line in processes:
		if 'mysql' in pscmd_line.lower():
			install_server_dict["DATABASE_SERVER"] = "MYSQL"
			running_process["DATABASE_SERVER"] = "MYSQL"
		elif 'mariadb' in pscmd_line.lower():
			install_server_dict["DATABASE_SERVER"] = "MARIADB"
			running_process["DATABASE_SERVER"] = "MARIADB"
		elif 'oracle' in pscmd_line.lower():
			install_server_dict["DATABASE_SERVER"] = "ORACLE"
			running_process["DATABASE_SERVER"] = "ORACLE"
		elif 'mongodb' in pscmd_line.lower():
			install_server_dict["DATABASE_SERVER"] = "MONGODB"
			running_process["DATABASE_SERVER"] = "MONGODB"
		elif 'httpd' in pscmd_line.lower():
			install_server_dict["WEB_SERVER"] = "APACHE"
			running_process["WEB_SERVER"] = "APACHE"
		elif 'nginx' in pscmd_line.lower():
			install_server_dict["WEB_SERVER"] = "NGINX"
			running_process["WEB_SERVER"] = "NGINX"

	return running_process

running_process = get_processes()

os_artifact_path = os.path.join('./', 'os_artifact')
os.makedirs(os_artifact_path, exist_ok = True)

process_path = os.path.join(os_artifact_path, 'run_process.json')
with open(process_path, 'w') as run_proc_result:
	json.dump(running_process, run_proc_result, indent = 4)


print("=> netstat analysis")
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


print("=> web server analysis")
document_root_list = []
if "APACHE" in install_server_dict["WEB_SERVER"]:
	httpd_conf_path_list = findfile('httpd.conf', '/')

	# httpd read
	if len(httpd_conf_path_list) > 0:
		for httpd_conf_path in httpd_conf_path_list:
			with open(httpd_conf_path, 'r') as httpd_conf:
				for httpd_conf_line in httpd_conf:
					if 'documentroot' in httpd_conf_line.lower():
						try:
							k, v = httpd_conf_line.strip().split(' ')
							if v.startswith('"'):
								v = v.strip('"')
	
							document_root_list.append(v)
						except:
							continue
elif "NGINX" in install_server_dict["WEB_SERVER"]:
	#TODO : nginx conf parser
	nginx_conf_path_list = findfile('nginx.conf', '/')

print("=> database server connected info analysis")
database_connect_info = {}
for document_root in document_root_list:
	# TODO : change to compare different values
	if 'codeigniter' in document_root.lower():
		document_root.lower()
	elif 'symfony' in document_root.lower():
		document_root_list = document_root.split('/')
		document_root_list.pop()

		env_path = os.path.join('/'.join(document_root_list), '.env')
		with open(env_path, 'r') as symfony_env:
			for symfony_env_line in symfony_env:
				if symfony_env_line.startswith('DATABASE_URL'):
					symfony_env_line = symfony_env_line.replace("\"", "")

					k, v = symfony_env_line.split("=", 1)
					database_url = v

		# TODO : database url parser 

	elif 'laravel' in document_root.lower():
		document_root_list = document_root.split('/')
		document_root_list.pop()

		env_path = os.path.join('/'.join(document_root_list), '.env')
		db_config_path = os.path.join('/'.join(document_root_list), 'config', 'database.php')
		
		env_dictionary = {}
		with open(env_path, 'r') as env:
			# .env file to dictionary
			for env_line in env:
				try:
					#print(env_line)
					(key, val) = env_line.split('=', 1)
					env_dictionary[key] = val
				except:
					continue

		key_stack = []
		value_stack = []
		with open(db_config_path, 'r') as db_config:
			for db_config_line in db_config:
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
				'''
				if value is None:
					print(key + ", ")
				else:
					print(key + ", " + value)
				'''

			# TODO : make dictionary

	elif 'wordpress' in document_root.lower():
		db_config_path = os.path.join(document_root, 'wp-config.php')
		with open(db_config_path, 'r') as db_config:
			for db_config_line in db_config:
				if re.search(r'define\(\s*\'(DB)|(db)|(Db)|(dB)', db_config_line):
					db_config_line = remove_define(db_config_line)
					#print(db_config_line)

					k, v = db_config_line.split(',')
					if "name" in k.lower():
						database_connect_info["DATABASE"] = v.strip()
					elif "user" in k.lower():
						database_connect_info["USER"] = v.strip()
					elif "password" in k.lower():
						database_connect_info["PASSWORD"] = v.strip()
					elif "host" in k.lower():
						database_connect_info["HOST"] = v.strip()
						


	elif 'gnuboard' in document_root.lower():
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
	json.dump(database_connect_info, result, indent = 4)

print("=> database backup")
database_backup_path = os.path.join('./', 'database_backup')
os.makedirs(database_backup_path, exist_ok = True)

now = datetime.datetime.now()
now = now.strftime("%Y%m%d%H%M%S")

#print(database_connect_info)
#print(install_server_dict)

dump_dst = os.path.join(database_backup_path, now+'_'+database_connect_info["DATABASE"]+'.sql')
dump_cmd = []
dump_cmd.append("./mysqldump")
dump_cmd.append("-u %s" % database_connect_info["USER"])
dump_cmd.append("-p%s" % database_connect_info["PASSWORD"])
dump_cmd.append("-h %s" % database_connect_info["HOST"])
dump_cmd.append("%s > " % database_connect_info["DATABASE"])
dump_cmd.append("%s" % dump_dst)
#os.system(" ".join(dump_cmd))
#process = os.popen(" ".join(dump_cmd))
dump_cmd_result = subprocess.Popen(" ".join(dump_cmd), shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
ps = dump_cmd_result.communicate()[0]

BUF_SIZE = 65536
md5 = hashlib.md5()
sha1 = hashlib.sha1()

with open(dump_dst, 'rb') as dump_file:
	while True:
		data = dump_file.read(BUF_SIZE)
		if not data:
			break

		md5.update(data)
		sha1.update(data)

print("MD5: {0}".format(md5.hexdigest()))
print("SHA1: {0}".format(sha1.hexdigest()))

hash_path = dump_dst +  '.hash'
with open(hash_path, 'w') as h:
	h.write("MD5: {0}".format(md5.hexdigest()))
	h.write("SHA1: {0}".format(sha1.hexdigest()))










