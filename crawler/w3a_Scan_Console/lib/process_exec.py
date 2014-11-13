#!/usr/bin/python
import multiprocessing
import time

class process_class:
	
	def __init__(self,process_sum):
		self.process_sum=process_sum
		self.exec_results=[]
		self.results=[]

	def _createProcess(self,fun,values):
		pool=multiprocessing.Pool(processes=self.process_sum)
		for item in values:
			self.exec_results.append(pool.apply_async(fun,(item,)))
		pool.close()
		pool.join()
	
	def _getResults(self):
		for item in self.exec_results:
			self.results.append(item.get())
		return self.results


#t=process_class(10)
#aa=['a','b','c','d','1',1,2,3,4,5,6,7,8,9,0,213123,3,23,23,2,312,312,3,12,31,23,12,3,123,1,231,3,1]
#t._createProcess(functer,aa)
#print t._getResults()
