
def find_file_list(name, path):
    filelist = []
	for dirpath, dirname, filename in os.walk(path):
		if name in filename:
			filelist.append(os.path.join(dirpath, name))

	return filelist