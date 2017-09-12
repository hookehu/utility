#-*- coding:utf-8	-*-
import paramiko
import dircache,os

class	SFTPSyncTool:
	host = '192.168.11.239'
	user = 'hooke'
	pwd	=	'123456'
	
	rpath	=	'pub/web'
	local_path = 'E:/v1'
	def __init__(self):
		pass
		
	def mkdir(self, path):
		ps = path.split('/')
		parent = '.'
		for f in ps:
			if f == "":
				print "path contain empty folder"
				break
			self.ftp.chdir(parent)
			names = self.ftp.listdir('.')
			if f in names:
				parent = f
				continue
			self.ftp.mkdir(f)
			parent = f
			
	def exe_cmd(self, cmd):
		stdin, stdout, stderr = self.ssh.exec_command(cmd)
		print(stdout.read().decode())
		
	def	login(self):
		self.trans = paramiko.Transport((self.host, 22))
		self.trans.connect(username=self.user, password=self.pwd)
		self.ssh = paramiko.SSHClient()
		ssh._transport = self.trans
		self.ftp = paramiko.SFTPClient.from_transport(self.trans)
		self.home = self.ftp.getcwd()
		self.mkdir(self.rpath)
		names = self.ftp.listdir('.')
		#print names
		
	def	sync_to_server(self):
		files	=	dircache.listdir(self.local_path)
		for	file in	files:
			p	=	self.local_path	+	'/'	+	file
			if os.path.isdir(p):
				self.sync_folder_to_server(p,	"",	file)
			else:
				self.sync_file_to_server(p,	file,	"")
		
	def	sync_folder_to_server(self,	path,	parent_dir,	folder_name):
		files	=	dircache.listdir(path)
		self.ftp.chdir(self.home)
		self.ftp.chdir(self.rpath)
		if parent_dir	!= "":
			self.ftp.chdir(parent_dir)
		names	=	self.ftp.listdir('.')
		if folder_name not in	names:
			self.ftp.mkdir(folder_name)
		for	file in	files:
			p	=	path + '/' + file
			if os.path.isdir(p):
				if parent_dir	!= "":
					self.sync_folder_to_server(p,	parent_dir + '/' + folder_name,	file)
				else:
					self.sync_folder_to_server(p,	folder_name, file)
			else:
				if parent_dir	!= "":
					self.sync_file_to_server(p,	file,	parent_dir + '/' + folder_name)
				else:
					self.sync_file_to_server(p,	file,	folder_name)
		
	def	sync_file_to_server(self,	file,	rname, parent_dir):
		self.ftp.chdir(self.home)
		self.ftp.chdir(self.rpath)
		if parent_dir	!= "":
			self.ftp.chdir(parent_dir)
		self.ftp.put(file, rname)
		
	def	sync_from_server(self):
		pass
		
	def	close(self):
		self.trans.close();

if __name__	== "__main__":
	ftp = SFTPSyncTool()
	ftp.login()
	ftp.sync_to_server()
	ftp.close()
	print ftp.local_path
	print	"success"