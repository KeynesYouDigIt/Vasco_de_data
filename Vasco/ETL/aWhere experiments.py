#meta data http://developer.awhere.com/integration/tutorials
#calls http://developer.awhere.com/api/get-started

#why use requests vs httplib2
#http://docs.python-requests.org/en/master/community/faq/

import requests as rq
import base64
#base64.b64encode(


Key = 'wwJN2yTlGEVzB2SAfnN7A5215B2Eshjj'
Secret = 'ksyXJbpbzRbGDObw'

def GetOAuthToken(key, secret):
    conn = httplib.HTTP(host)
    conn.putrequest('POST', '/oauth/token')
    conn.putheader("Content-type", "application/x-www-form-urlencoded")
    
    auth = base64.encodestring('%s:%s' % (Key, Secret)).replace('\n', '')
    conn.putheader("Authorization", "Basic %s" % auth)
    conn.endheaders()
    conn.send(message)
    statuscode, statusmessage, header = conn.getreply() 
    
    res = conn.getfile().read()
    #return the access token from the json response
    return res


do = GetOAuthToken(Key, Secret)
##InvalidURL: nonnumeric port: '//api.awhere.com'



#####
######

authhed = 'Basic ' + base64.b64encode('%s:%s' % (Key, Secret)) .replace('\n', '')

auth_url = 'https://api.awhere.com/oauth/token'

auth_headers = {'Authorization':authhed, 'Content-Type': 'application/x-www-form-urlencoded'}



authr = rq.Request('POST', auth_url, data="grant_type=client_credential", headers=auth_headers)

authrp  = authr.prepare()

s = rq.Session()

resp = s.send(authrp)



#######
auth=rq.post(auth_url, 
    headers = auth_headers,
    data = "grant_type=client_credential")

header_w_auth= {'Authorization':'Bearer' + auth.content}

call_host = 'https://api.awhere.com'
basic_uri = '/v1/weather?latitude=40&longitude=-95&startDate=2015-05-01'

get_dat = rq.get(call_host+basic_uri,
    headers = header_w_auth)

In [21]: auth.content
Out[21]: '{"access_token":"","expires_in":}'





In [176]: auth.headers
Out[176]: {'Content-Length': '33', 
'Accept-Encoding': 'gzip, deflate', 
'X-Forwarded-Port': '443', 'X-Forwarded-For': '73.14.31.29', 
'Accept': '*/*', 'Server': 'Apigee Router', 'Connection': 'keep-alive', 
'X-Forwarded-Proto': 'https', 'Date': 'Sat, 12 Nov 2016 17:59:02 GMT', 
'User-Agent': 'python-requests/2.9.1', 'Content-Type': 'application/json', 
'Authorization': 'Basic d3dKTjJ5VGxHRVZ6QjJTQWZuTjdBNTIxNUIyRXNoamo6a3N5WEpicGJ6UmJHRE9idw=='}


example = base64.b64encode('ABCDEFG:123456')

'QUJDREVGRzoxMjM0NTY='
'QUJDREVGRzoxMjM0NTY='