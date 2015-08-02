#!/usr/bin/env python
#coding:utf-8

import Image,ImageFont,ImageDraw,ImageFilter
import os,sys
from math import atan2,pi,sqrt
import cPickle as pickle

#import psyco
#psyco.full()

DURATION = 1000
DIAMETER = 20
COLORDIFF = 10
TEXTCOLOR = 128
BACKGROUND = 255
DBFILE='sina.pk'
MODE = 'sample'
samples = None


def pixelcount(region):		
	frame=region.load()
	(w,h)=region.size
	count=0
	for i in xrange(w):
		for j in xrange(h):
			if frame[i,j]!=BACKGROUND:
				count+=1
	return count			

def printregion(region):
	frame = region.getdata()
	(w,h)=region.size
	for i in xrange(h):
		for j in xrange(w):
			if frame[i*w+j] != BACKGROUND:
				print '*',
			else:
				print ' ',
		print

def purify(region):
	frame = region.getdata()
	(w,h)=region.size
	for i in xrange(h):
		for j in xrange(w):
			if frame[i*w+j] != BACKGROUND:
				region.putpixel( (j,i), TEXTCOLOR )
			else:
				region.putpixel( (j,i), BACKGROUND )
	return region


def isdot(frame,pos):
	(x,y)=pos	
	color=frame[x,y]
	count=0
	try:
		if dist3d(frame[x,y-1],color)>5:
			count+=1
	except:
		pass
	try:
		if dist3d(frame[x,y+1],color)>5:
			count+=1
	except:
		pass
	try:
		if dist3d(frame[x-1,y],color)>5:
			count+=1
	except:
		pass
	try:
		if dist3d(frame[x+1,y],color)>5:
			count+=1
	except:
		pass
	try:
		if dist3d(frame[x-1,y-1],color)>5:
			count+=1
	except:
		pass
	try:
		if dist3d(frame[x+1,y-1],color)>5:
			count+=1
	except:
		pass
	try:
		if dist3d(frame[x+1,y+1],color)>5:
			count+=1
	except:
		pass		
	try:
		if dist3d(frame[x-1,y+1],color)>5:
			count+=1
	except:
		pass
	if count<3:

		return False
	else:
		return True
		


def floodfillfilter(im,way=4,mincount=8):
	frame=im.load()
	(w,h)=im.size
	points=[]
	processedpoints=[]
	global goodpoints
	goodpoints=[]	
	for x in xrange(w):
		for y in xrange(h):
			color=frame[x,y]
			if color==BACKGROUND or ((x,y) in processedpoints):
				continue
			processedpoints.append((x,y))	
			
			points.append((x,y))
			
			#points.remove((x,y))
			for (x,y) in points:
				
				try:
					if frame[x,y-1] ==color and (x,y-1) not in points:
						points.append((x,y-1))						
				except:
					pass
				try:
					if frame[x,y+1] ==color and (x,y+1) not in points:
						points.append((x,y+1))						
				except:
					pass
				try:
					if frame[x-1,y] ==color and (x-1,y) not in points:
						points.append((x-1,y))						
				except:
					pass	
				try:
					if frame[x+1,y] ==color and (x+1,y) not in points:
						points.append((x+1,y))						
				except:
					pass
				if way==8:
					try:
						if frame[x-1,y-1]==color and (x-1,y-1) not in points:
							points.append((x-1,y-1))							
					except:
						pass			
					try:
						if frame[x+1,y-1]==color and (x+1,y-1) not in points:
							points.append((x+1,y-1))							
					except:
						pass
					try:
						if frame[x-1,y+1]==color and (x-1,y+1) not in points:
							points.append((x-1,y+1))							
					except:
						pass
					try:
						if frame[x+1,y+1]==color and (x+1,y+1) not in points:
							points.append((x+1,y+1))							
					except:
						pass
			processedpoints.extend(points)
			#print color,len(points)
			#print points
			if 1<len(points)<mincount:
				for (x,y) in points:
					#print x,y
					frame[x,y]=BACKGROUND
			if len(points)>16:
				goodpoints.extend(points)				
			
			points=[]
			
	#im.show()
	return im	
		
		
def removedot(im):
	#global goodpoints
	frame=im.load()
	(w,h)=im.size
	for i in xrange(w):
		for j in xrange(h):
			if frame[i,j]!=255:
				count=0
				try:
					if frame[i,j-1]==255:
						count+=1
				except IndexError:
					pass		
				try:
					if frame[i,j+1]==255:
						count+=1
				except IndexError:
					pass
				try:
					if frame[i-1,j-1]==255:
						count+=1
				except IndexError:
					pass
				try:
					if frame[i-1,j]==255:
						count+=1
				except IndexError:
					pass	
				try:	
					if frame[i-1,j+1]==255:
						count+=1
				except IndexError:
					pass
				try:
					if frame[i+1,j-1]==255:
						count+=1
				except IndexError:
					pass	
				try:	
					if frame[i+1,j]==255:
						count+=1
				except IndexError:
					pass
				try:
					if frame[i+1,j+1]==255:
						count+=1
				except IndexError:
					pass
				
				if count>=6:
					frame[i,j]=BACKGROUND

	return im
			
	
def distance(r1,r2):
	den1 = density(r1)
	den2 = density(r2)
	if 1.0*den1/den2>1:
		(den1,den2) = (den2,den1)
	r1 = r1.resize(r2.size)	
	d1 = r1.getdata()
	d2 = r2.getdata()
	same = [0,0]
	total = [0,0]
	for i in xrange(len(d1)):
		if d1[i] != BACKGROUND:
			total[0] += 1
			if d1[i] == d2[i]:
				same[0] += 1
		if d2[i] != BACKGROUND:
			total[1] += 1
			if d1[i] == d2[i]:
				same[1] += 1
	try:	
		return 1 - 1.0*same[0]/total[0] * 1.0*same[1]/total[1] * 1.0*den1/den2
	except:
		return 1
	
def getframe(fname,strict=1):
	'''return w*h key frame without noise'''
	#open image
	try:
		im = Image.open(fname)
	except:
		return "File error!"
	frame = im.load()
	(w,h)=im.size

	for i in xrange(w):
		frame[i,0]=(255,255,255)
		frame[i,h-1]=(255,255,255)
	
	for i in xrange(h):
		frame[0,i]=(255,255,255)
		frame[w-1,i]=(255,255,255)
		
	for i in xrange(w):
		for j in xrange(h):
			if frame[i,j]>(200,200,200):
				frame[i,j]=(255,255,255)
			if frame[i,j]!=(255,255,255):
				frame[i,j]=(0,0,0)
	im=im.convert('L')	
	im=removedot(im)
	im=floodfillfilter(im,4,20)
	#im.show()
	return im

def loadsamples():
	pks = pickle.load(open(DBFILE,'rb'))
	samples = {}
	for (pk,v) in pks.items():
		im = Image.new('L',pk[0])
		r = im.crop((0,0,pk[0][0],pk[0][1]))
		r.fromstring(pk[1])
		samples[r] = v
	return samples


def match(region,samples):
#	printregion( region )
	if samples == {}:
		return None
	dists = []
	for (k,v) in samples.items():
		dists.append( (distance(region,k),v) )
	dists.sort()

	if MODE == 'sample':
		return dists[0][1]
	else:
		i = 0
		while dists[i][1] in ['H','I']:
			i += 1
		return dists[i][1]
#	printregion( region )
#	printregion( samples[ dists[0][1] ] )

def trainmatch(region,samples):
	if samples == {}:
		return None
	dists = []
	for (k,v) in samples.items():
		dists.append( (distance(region,k),v) )
	dists.sort()	
	confidence=1-dists[0][0]	
	first=dists[0][1]
	for i in xrange(1,4):
		if dists[i][1]==first:
			confidence+=0.05
			
		
	if confidence<0.75:
		for i in xrange(0,10):
			print dists[i]
	
	if MODE == 'sample':
		return [dists[0][1],confidence]
	else:
		i = 0
		while dists[i][1] in ['H','I']:
			i += 1
		return [dists[i][1],confidence]
#	printregion( region )
#	printregion( samples[ dists[0][1] ] )


def imdiv(im):
	'''div and return pieces of pics'''
	frame = im.load()
	(w,h) = im.size
	horis =  []
	for i in xrange(w):
		for j in xrange(h):
			if frame[i,j] != BACKGROUND:
				horis.append(i)
				break
	
	horis2 = [max(horis[0]-2,0)]
	for i in xrange(1,len(horis)-1):
		if horis[i]!=horis[i+1]-1:
			horis2.append((horis[i]+horis[i+1])/2)
	horis2.append(min(horis[-1]+3,w))
	boxes=[]
	for i in xrange(len(horis2)-1):
		boxes.append( [horis2[i],0,horis2[i+1],h]  )
	for k in xrange(len(boxes)):
		verts = []
		for j in xrange(h):
			for i in xrange(boxes[k][0],boxes[k][2]):
				if frame[i,j] != BACKGROUND:
					verts.append(j)
		boxes[k][1] = max(verts[0]-2,0)
		boxes[k][3] = min(verts[-1]+3,h)
	if boxes == []:
		return None
	regions = []
	for box in boxes:
		regions.append( im.crop(box) )
	return regions
	
def getcrop(region):
	frame = region.getdata()
	(w,h)=region.size
	pts = []
	ptsi = []
	for i in xrange(h):
		for j in xrange(w):
			if frame[i*w+j] != BACKGROUND:
				pts.append((i,j))
				ptsi.append((j,i))
	if pts == []:
		return [0,0,1,1]
	pp1 = min(pts)
	pp2 = max(pts)
	pp3 = min(ptsi)
	pp4 = max(ptsi)
	return [pp3[0],pp1[0],pp4[0]+1,pp2[0]+1]

def density(region):
	frame = region.getdata()
	(w,h) = region.size
	area_all = w*h
	area = 0
	for i in xrange(h):
		for j in xrange(w):
			if frame[i*w+j] != BACKGROUND:
				area += 1
	return 1.0*area/area_all

def docrop(region):
	croppos = getcrop(region)
	newregion = region.crop(croppos)
	#newregion.show()
	return newregion

def dorotate(region):
#	printregion(region)
	deg = 0
	maxdens = 0
	for i in xrange(-15,15):
		dens = density( docrop( region.rotate(i) ) )
		if dens > maxdens:
			deg = i
			maxdens = dens
			
	#	printregion( docrop( region.rotate(deg) ) )
	return region.rotate(deg)

def normalize(im):
	# divide im
	regions = imdiv(im)
	for k in xrange(len(regions)):
		regions[k] = dorotate(regions[k])
		regions[k] = purify( docrop(regions[k]) )
	
	return regions

def train(im):
	global samples
	try:
		samples = pickle.load(open(DBFILE,'rb'))
	except:
		samples = {}
		pickle.dump(samples,open(DBFILE,'wb'))

	regions = normalize(im)
	for region in regions:
		if pixelcount(region)<=20:
			continue
		(w,h)=region.size
#		region = region.resize((w*.8,h*.8))
		printregion(region)
		#''' Comment this section when no data to begin with
		smps = loadsamples()
		matchresult=trainmatch(region,smps)
		if matchresult!=None:
			result=matchresult[0]
			confidence=matchresult[1]
			print "Confidence:"+str(confidence)
			print result.upper()
			if confidence>=0.75:
				continue
		else:
			print "No match data, please input"
		
		#'''
		#im.show()	
		print 'enter [0-9a-z] to add to library: '
		ans = raw_input()
		if len(ans) == 1:
			key = (region.size,region.tostring())
			samples[key] = ans[0]
			pickle.dump(samples,open(DBFILE,'wb'))

def crackcode(im):
	global samples
	if not samples:
		samples = loadsamples()
	regions = normalize(im)
	s = []
	ans = []
	for r in regions:
		if pixelcount(r)<=20:
			continue
		value=match(r,samples).upper()
		if value!=' ':
			s.append(value)

	if len(s) != 5:
		return ['failed']
	else:
		for s1 in s[0]:
			for s2 in s[1]:
				for s3 in s[2]:
					for s4 in s[3]:
						for s5 in s[4]:
							t = s1+s2+s3+s4+s5
							ans.append(t)
	return ans
	

if __name__ == '__main__':
	if len(sys.argv)==1:
		exit('Usage: sina.py filename.png')
	if len(sys.argv) == 2:
		if sys.argv[1].startswith('train'):
			trainfiles = os.listdir(sys.argv[1])
			#trainfiles.sort()
			for trainfile in trainfiles:
				trainfile = sys.argv[1]+'/'+trainfile
				print trainfile
				im = getframe(trainfile)
				train(im)
				os.remove(trainfile)
		else:
			filename=sys.argv[1]
			extension=os.path.splitext(filename)[1]
			#print extension
			if MODE == 'sample':
				samples = loadsamples()
			else:
				samples = loadttf()
			results = {}
			im = getframe(filename)
			#im.show()
			#printframe(im)
			ans = crackcode(im)
			#print ans
			if 'failed' in ans:
				im = getframe(filename,1)
				ans = crackcode(im)
			for result in ans:
				print result
			
