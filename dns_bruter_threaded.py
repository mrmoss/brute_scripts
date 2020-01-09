#!/usr/bin/env python2
#  pip install dnspython

#Example usages:
#  cat dict.txt|./dns_bruter_threaded.py
#  john --incremental -stdout=8|./dns_bruter_threaded.py
import dns.resolver
import pool_manager
import sys

try:
	input=raw_input
except Exception:
	pass

#returns (INT,STR)
#  INT is either 1 fail, 0 success, or -1 error
#  STR is error string or success string
def dns_query(lookup,nameserver='8.8.8.8'):
	try:
		resolver=dns.resolver.Resolver()
		resolver.nameserver=[nameserver]
		dns.resolver.query(lookup)
		return (0,'Success')
	except (dns.resolver.NXDOMAIN,dns.exception):
		return (1,'Not found.')
	except dns.resolver.Timeout:
		return (-1,'Timeout')

def worker(pool_man,domain,nameserver):
	try:
		while not pool_man.is_done():
			subdomain=pool_man.pop()
			if subdomain!=None:
				test=dns_query(subdomain+'.'+domain,nameserver)
				if not pool_man.is_done():
					pool_man.show(subdomain+'.'+domain+'\t'+test[1])
					if test[0]==-1:
						pool_man.set_result(test)
	except Exception:
		pass

pool_man=pool_manager.pool_manager_t()

if __name__=='__main__':
	if len(sys.argv)<2:
		print('Usage: '+sys.argv[0]+' DOMAIN [THREADS] [DNS_SERVER]')
		exit(1)
	try:
		thread_count=8
		if len(sys.argv)>2:
			thread_count=int(sys.argv[2])
		nameserver='8.8.8.8'
		if len(sys.argv)>3:
			nameserver=sys.argv[3]
		print('Starting dns brute force ('+str(thread_count)+' threads)')
		for ii in range(thread_count):
			pool_man.new(worker,(sys.argv[1],nameserver))
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
