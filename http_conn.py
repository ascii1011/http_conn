#!/usr/bin/python2.7 -tt

import sys
import re
import httplib
from urlparse import parse_qs, urlsplit
from urllib import urlencode, quote, quote_plus
from datetime import datetime

### for testing only
from pprint import pprint

class HTTPcn(object):
	"""
	Created By Christopher Harty

	HTTPcn is a reusable tool for requesting and capturing 
	responses specific to pixel tracking
	
	Inputs:
		'url': url,
		'data': data,
		'auth': auth,
		'headers': headers,
		'requestType': 'POST',
		'returnFormat': 'xml',
		'DEBUG': 'True',
   
	Internal Use Case:
		 h=HttpConn(url)
		 def do_request(url, param, headers={}):
			 return HTTPcn( {'url': url, 'data': param, '}).request()
			 
		 from MyLib.utilities.http import do_request
	""" 
    
    def __init__(self, params={}):  
        #init
        self._url( params.get('url') )
        self._data( params.get('data') )
        self._headers( params.get('headers') )
        self._auth( params.get('auth') )
        self.timeout = params.get('timeout', 1)
        self.params = ''
        
        #put it all together                
        self._urlEncode()
        self._get_headers()
        self._get_conn()
               
        #response
        self.status = ''
        self.resHeaders = ''
        self.raw = ''
        self.res = ''

        self.debug = {}
        
    def _auth(self, auth):
        if isinstance(auth, dict):
            self.auth = auth
        else:
            self.auth = dict()
        
    def _headers(self, headers):
        if isinstance(headers, dict):
            self.headers = headers
        else:
            self.headers = dict()
          
    def _data(self, data):
        if isinstance(data, dict):
            self.data = data
        else:
            self.data = dict()
           
    def _url(self, url):
        self.url = url
        self.parts = []
        if self.url:
            self.parts = urlsplit( self.url )
        
    def _urlEncode(self):
        if isinstance(self.data, str ):
            self.params = self.data
        else:
            self.params = urlencode( self.data, True )
    
    def _get_conn(self):
        if self.parts.scheme == 'https':
            self.cc = httplib.HTTPSConnection
        else:
            self.cc = httplib.HTTPConnection
    
    def _get_headers(self):
		# this portion has been omited
        self.headers['Content-Length']=str(len(self.params))
        self.headers['host']='' 
        self.headers['Connection']='close'
		
           
    def request(self):
        res = ''
        if not self.debug:
            res = self._do_conn()
        return res
                
    def _do_conn(self):
		result = None
		# this portion has been omited
        try:
            # this portion has been omited
			result = 1
        except Exception, e:
            self.debug['_do_conn'] = e
            failed=True
            
            result = ( self.status, self.resHeaders, e )
            raise Exception( 'HTTPcn error: %s' % str( e ) )
        
        else:
            result = ( self.status, self.resHeaders )
        
        finally:
            conn.close()
            return result
                    
    def _parse(self):
        self.raw = re.sub("[\n\t\r]", "", self.raw)
        self.res = self.parse_ping( self.raw )
        
    def get_raw(self):
        return self.raw
    
    def get_res(self):
        return self.res

    def print_debug_init(self):
        print 'url: %s' % self.url
        print 'headers: %s' % self.headers
        print 'auth: %s' % self.auth
        print 'timeout %s' % self.timeout
        print 'data:'
        pprint(self.data)
        print 'parts:'
        pprint(self.parts)
        
    def print_debug_end(self):
        print 'raw: %s' % self.raw
        print 'res: %s' % self.res
        
    def print_debug(self):
        print 'debug:'
        pprint(self.debug)
        
    
def httplib_test_v2(data):
    import httplib, urllib
    params = urllib.urlencode(data)
    host = "copmanyb.com"
    path = "/api/v112/subscribers"
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Content-Length":str(len( params )),
        "X-Forwarded-Ssl": "on",
        "X-API-KEY": "33af9dcfesfsecb0d89fc4a7asfse08042ebc70826asef",
        }
    
    print params
    pprint( headers )
    
    conn = httplib.HTTPSConnection(host)
    conn.request("POST", path, params, headers)

    response = conn.getresponse()
    
    print response.status, response.reason

    data = response.read()
    print 'response.read: %s' % str(data)
    conn.close()
    
        
if __name__ == "__main__":
    data = {"email":"some@emailaddress.com",
            "channel":["CompanyC-national",],
            "format":"xml",}
    httplib_test_v2(data)
