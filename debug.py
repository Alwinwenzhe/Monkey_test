import os
def get_file_path(root_path, file_list, dir_list):
	# 获取该目录下所有的文件名称和目录名称
	dir_or_files = os.listdir(root_path);
	for dir_file in dir_or_files:
		# 获取目录或者文件的路径
		dir_file_path = os.path.join(root_path, dir_file)
		# 判断该路径为文件还是路径
		if os.path.isdir(dir_file_path):
			dir_list.append(dir_file_path)
			# 递归获取所有文件和目录的路径
			get_file_path(dir_file_path, file_list, dir_list)
		else:
			os.remove(root_path + dir_file)

if __name__ == '__main__':
	file_list = []
	dir_list = []
	root_path = os.path.abspath(os.path.dirname(__file__)) + r'\bugreport_out' + r"\com.jmbon.android"
	get_file_path(root_path,file_list,dir_list)