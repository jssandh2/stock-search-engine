
# Function required for backend operation
# Bing, NLP and Scoring

import json, requests, urllib, urllib2, logging, base64

url = "https://api.datamarket.azure.com/Bing/Search/v1/News?Query=%27apple%27&Market=%27en-US%27&NewsCategory=%27rt_Business%27&NewsSortBy=%27Relevance%27"

BingKey = "jpADODPO6cElNoSZefCKhWntzIuoN27NWTN+pU0rltc"

apikey = '979e3fc42bc01cce4549f93c1e5ef3311665ecc4' # alchemy apikey

def auth_extract(url):
    url_base = 'http://access.alchemyapi.com/calls/url/URLGetAuthor'
    url_settings = '?apikey=' + apikey + '&outputMode=json&url='
    r = requests.get(url_base + url_settings + url)
    result = json.loads(r.text)
    return result

def basicNewSearch(query, skip):
    username = '9adffa4f-0bb2-4a22-a308-aa2d36ba0435'
    password = 'jpADODPO6cElNoSZefCKhWntzIuoN27NWTN+pU0rltc'
    url = "https://api.datamarket.azure.com/Bing/Search/v1/News?Query=%27"+query+"%27&Market=%27en-US%27&NewsCategory=%27rt_Business%27&NewsSortBy=%27Relevance%27&$format=json&$skip="+str(skip)
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    result = urllib2.urlopen(request).read()
    return result

def test(query):
    return final_call.main_call_function('tesla')
    #return "Test dsafdsafas Function"
