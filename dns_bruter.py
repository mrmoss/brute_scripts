#!/usr/bin/env python
#  pip install dnspython

#Example usages:
#  cat dict.txt|./dns_bruter.py
#  john --incremental -stdout=8|./dns_bruter.py
import dns.resolver
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

if __name__=='__main__':
	if len(sys.argv)<2:
		print('Usage: '+sys.argv[0]+' DOMAIN [DNS_SERVER]')
		exit(1)
	nameserver='8.8.8.8'
	if len(sys.argv)>2:
		nameserver=sys.argv[2]
	print('Starting dns brute force')
	try:
		while True:
			subdomain=input('')
			sys.stdout.write(subdomain+'.'+sys.argv[1]+'\t')
			sys.stdout.flush()
			test=dns_query(subdomain+'.'+sys.argv[1],nameserver)
			sys.stdout.write(test[1]+'\n')
			sys.stdout.flush()
			if test[0]==-1:
				exit(1)
	except KeyboardInterrupt:
		exit(1)
	except EOFError:
		exit(1)
	except Exception as error:
		print(error)
		exit(1)