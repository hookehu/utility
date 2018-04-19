#-*- coding:utf-8	-*-
import paramiko
import dircache,os
import hashlib, time
import select

class	SniferTool:
		host = '192.168.11.111'
		user = 'root'
		pwd	=	'Root!@#456'
		
		def __init__(self):
				pass
				
		def exe_cmd(self, cmd):
				stdin, stdout, stderr = self.ssh.exec_command(cmd)
				#rst = stdout.read().decode()
				#err = stderr.read().decode()
				print(stdout.read())
				#while True:
				#		print(stdout.read())
			
		def	proc(self):
				self.trans = paramiko.Transport((self.host, 22))
				self.trans.connect(username=self.user, password=self.pwd)
				self.ssh = paramiko.SSHClient()
				self.ssh._transport = self.trans
				channel = self.trans.open_session()
				channel.get_pty()
				cmd = 'python3 ~/snifer/snifer.py Avatar s dst net 192.168.11.111 and tcp and port 20351'
				channel.exec_command(cmd)
				while True:
						if channel.exit_status_ready():
								break
						try:
								rl,wl,xl=select.select([channel],[],[],1)
								if	len(rl)>0:
										recv=channel.recv(65536)
										print recv
		
						except	KeyboardInterrupt:
								print("Caught control-C")
								self.close()
								try:
										# open	new	socket and kill	the	proc..
										print("fff")
										#s.get_transport().open_session().exec_command(
										#		"pkill	-9 tail"
										#)
								except:
										pass
								exit(0)

		def	close(self):
				self.trans.close();

if __name__	== "__main__":
	t = SniferTool()
	t.proc()
	print	"success"