#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json


def http_post(url, values):
    """TODO: POST method.
    :url: http url(string), such as "http://api.csdn.net/blog/savearticle"
    :values: post data(dict), such as {'access_token':'','title':'new post', 'content':'Test' }
    :return: result from server
    """
    jdata = json.dumps(values)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()

def oauth2():
    url = "http://api.csdn.net/oauth2/access_token"
    YOUR_API_KEY = '1100409'
    YOUR_API_SECRET = 'adce59b2ecc243519c6b55cdf43525e1'
    USER_NAME = 'DuinoDu'
    PASSWORD = '8460637duyuan'
    values = {'client_id':YOUR_API_KEY, 'client_secret':YOUR_API_SECRET, 'grant_type':'password', 'username':USER_NAME, 'password':PASSWORD }
    return http_post(url, values)

def AddNewArticle():
    url = "http://api.csdn.net/blog/savearticle"
    values = {'access_token':'','title':'new post', 'content':'Test' }
    return http_post(url, values)

#print AddNewArticle()
print oauth2()
