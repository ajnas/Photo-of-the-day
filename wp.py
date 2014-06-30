import httplib,urllib,json,os
pagename='Fcbarcelona'
appid='1454560308115172'
appsecret='cc39f36bc01b4843e0d7be0d428dddb6'
params = urllib.urlencode({'client_id':appid, 'client_secret': appsecret, 'grant_type': 'client_credentials'})
url="/oauth/access_token?"+params
print "Connecting to Facebook"
fb=httplib.HTTPSConnection("graph.facebook.com")
print "Requesting access token"
fb.request("GET",url)
response=fb.getresponse().read()
print "Parsing access token"
access_token=response[13:]
page_id_query="SELECT page_id FROM page WHERE username='"+pagename+"'"
params=urllib.urlencode({'q':page_id_query,'access_token':access_token})
url="/fql?"+params
print "Fetching page id "
fb.request("GET",url)
print "Parsing page_id"
response=fb.getresponse().read()
response=json.loads(response)
page_id=response['data'][0]['page_id']
params=urllib.urlencode({'limit':10,'access_token':access_token})
url="/"+page_id+"/posts/?"+params
print "Fetching last 10 timeline posts"
fb.request("GET",url)

print "Parsing posts"
response=fb.getresponse().read()
response=json.loads(response)
posts=response['data']
print "Seaking for photos"
photo_id=None
count=0
for post in posts:
	count=count+1
	if post['type']=='photo':
		print "Photo found "
		photo_id=post['object_id']
		break
	else:
		print "No photos in the last "+str(count)+" posts"

if photo_id:
	url="/"+photo_id
	print "Fetching Image Url"
	fb.request("GET",url)
	print "Parsing Image Url"
	response=fb.getresponse().read()
	response=json.loads(response)
	image_url=response['source']
	print "Downloading new image"
	urllib.urlretrieve (image_url, "sample.jpg")
	print "Downloading completed"
	print "Setting wallpaper"
	os.system("gsettings set org.gnome.desktop.background picture-uri file:///home/ajnas/dev/wp/Photo-of-the-day/sample.jpg")

else:
	print "Couldn't find any photos in the given page, please try after some time"

