#!/usr/bin/env python

import subprocess
import os
allFileNum = 0
outfile=''
file= ['h']

def printPath(level,path):
	global allFileNum
	dirList = []
	fileList = []
	files = os.listdir(path)

	dirList.append(str(level))
	for f in files:
		if(os.path.isdir(path+'/'+f)):
			if (f[0] == '.') :
				pass
			else:
				dirList.append(f)
		if(os.path.isfile(path+'/'+f)) and f.endswith(('.h','.m','.mm','.scala' )):
			fileList.append((path+'/'+f))
	
	i_dl = 0
	for dl in dirList:
		if(i_dl == 0) :
			i_dl = i_dl +1
		else:
			print '-'*(int(dirList[0])),dl
			subprocess.Popen("echo  %s >> /var/lib/jenkins/code/%s" % (dl,outfile),shell=True,stdout=subprocess.PIPE).stdout.readline()
			printPath((int(dirList[0])+1),path+'/'+dl)

	for fl in fileList:
		print '-' * (int(dirList[0])),fl
		subprocess.Popen("echo  %s >> /var/lib/jenkins/code/%s" % (fl,outfile),shell=True,stdout=subprocess.PIPE).stdout.readline()
		subprocess.Popen("cat   %s >> /var/lib/jenkins/code/%s" % (fl,outfile),shell=True,stdout=subprocess.PIPE).stdout.readline()
		allFileNum = allFileNum +1

if __name__ == '__main__':
	filepath = raw_input('file path: ')
	outfile = raw_input('outputfile name: ')
	printPath(1,filepath)
	print 'all file=',allFileNum
