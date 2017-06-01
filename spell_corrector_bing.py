# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:18:17 2017

@author: Shanika Ediriweera
"""

import http.client, urllib.request, urllib.parse, urllib.error, base64
#import urllib3.request, urllib3.parse, urllib3.error

headers = {
    # Request headers
    'Content-Type': 'application/x-www-form-urlencoded',
    #'Ocp-Apim-Subscription-Key': '{subscription key}',
    'Ocp-Apim-Subscription-Key': '4f44263fa15e4203920250272f62cc4e',
}

params = urllib.parse.urlencode({
    # Request parameters
    'mode': 'proof',
    'mkt': 'en-us',
})

body = "text=Would+have+been+butter+if+we+discussed+more+about+the+slutions+of+coding+exercisers"

try:
    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
    conn.request("POST", "/bing/v5.0/spellcheck/?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    #print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print("[Errno {0}] {1}",e)
    '''
conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
conn.request("POST", "/bing/v5.0/spellcheck/?%s" % params, bodyy, headers)
#response = conn.getresponse()
#data = response.read()
#print(data)
#conn.close()
'''
