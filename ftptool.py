#-*- coding:utf-8 -*-
import ftplib
import dircache,os

class FTPSyncTool:
	host = 'ftpip'#ftpµÿ÷∑
	user = 'ftpusername'#ftp’ ∫≈
	pwd = 'ftppasswd'#ftp√‹¬Î
	
	rpath = 'pub/web/h5'
	local_path = 'E:/pathtolocal'
	
	def __init__(self):
		pass
		
	def login(self):
		self.ftp = ftplib.FTP()
		self.ftp.connect(self.host)
		self.ftp.login(self.user, self.pwd)
		print self.ftp.getwelcome()
		names = self.ftp.nlst()
		
	def sync_to_server(self):
		files = dircache.listdir(self.local_path)
		for file in files:
			p = self.local_path + '/' + file
			if os.path.isdir(p):
				self.sync_folder_to_server(p, "", file)
			else:
				self.sync_file_to_server(p, file, "")
		
	def sync_folder_to_server(self, path, parent_dir, folder_name):
		files = dircache.listdir(path)
		self.ftp.cwd('/')
		self.ftp.cwd(self.rpath)
		if parent_dir != "":
			self.ftp.cwd(parent_dir)
		names = self.ftp.nlst()
		if folder_name not in names:
			self.ftp.mkd(folder_name)
		for file in files:
			p = path + '/' + file
			if os.path.isdir(p):
				if parent_dir != "":
					self.sync_folder_to_server(p, parent_dir + '/' + folder_name, file)
				else:
					self.sync_folder_to_server(p, folder_name, file)
			else:
				if parent_dir != "":
					self.sync_file_to_server(p, file, parent_dir + '/' + folder_name)
				else:
					self.sync_file_to_server(p, file, folder_name)
		
	def sync_file_to_server(self, file, rname, parent_dir):
		self.ftp.cwd('/')
		self.ftp.cwd(self.rpath)
		if parent_dir != "":
			self.ftp.cwd(parent_dir)
		f = open(file, "rb")
		self.ftp.storbinary('STOR ' + rname, f)
		f.close()
		
	def sync_from_server(self):
		pass
		
	def close(self):
		print self.ftp.getwelcome()
		self.ftp.quit()

if __name__ == "__main__":
	ftp = FTPSyncTool()
	ftp.login()
	ftp.sync_to_server()
	ftp.close()
	print "success"
