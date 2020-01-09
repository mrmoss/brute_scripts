#!/usr/bin/env python2
import sys
import threading
import time

class pool_manager_t:
	def __init__(self):
		self.threads=[]
		self.queue=[]
		self.result=(1,'None')
		self.finished=False

		self.queue_mutex=threading.Lock()
		self.result_mutex=threading.Lock()
		self.io_mutex=threading.Lock()

	def new(self,worker,args):
		new_thread=threading.Thread(target=worker,args=(self,)+args)
		new_thread.start()
		self.threads.append(new_thread)

	def add(self,data):
		self.queue_mutex.acquire()
		self.queue.insert(0,data)
		self.queue_mutex.release()

	def pop(self):
		data=None
		self.queue_mutex.acquire()
		if len(self.queue)>0:
			data=self.queue.pop()
		self.queue_mutex.release()
		return data

	def show(self,data):
		if not self.is_done():
			self.io_mutex.acquire()
			sys.stdout.write(data+'\n')
			sys.stdout.flush()
			self.io_mutex.release()

	def set_result(self,result):
		self.result_mutex.acquire()
		self.result=result
		self.finished=True
		self.result_mutex.release()

	def get_result(self):
		self.result_mutex.acquire()
		result=self.result
		self.result_mutex.release()
		return result

	def is_done(self):
		self.result_mutex.acquire()
		finished=self.finished
		self.result_mutex.release()
		return finished

	def wait(self):
		while True:
			try:
				for tt in self.threads:
					tt.join()
				break
			except Exception:
				pass
		return self.get_result()
