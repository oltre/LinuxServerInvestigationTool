# operating system check

import os

# history file find
def findfile(name, path):
	filepathlist = []
	for dirpath, dirname, filename in os.walk(path):
		if name in filename:
			#print(os.path.join(dirpath, name))
			filepathlist.append(os.path.join(dirpath, name))

	return filepathlist

# backup
#shutil.copy2("/etc/os-release", "./os-release")

# calc hash value(MD5, SHA1)

#httpd conf find
httpd_conf_path_list = findfile('httpd.conf', '/')

# httpd read
document_root_list = []
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
				

print(document_root_list)
