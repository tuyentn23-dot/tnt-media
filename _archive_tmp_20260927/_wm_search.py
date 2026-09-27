import urllib.request, urllib.parse, json
q=urllib.parse.quote('Mona Lisa Leonardo')
url='https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrsearch='+q+'&gsrlimit=3&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=1280'
req=urllib.request.Request(url, headers={"User-Agent":"TNTMedia/1.0"})
d=json.loads(urllib.request.urlopen(req,timeout=60).read().decode())
pages=d.get('query',{}).get('pages',{})
for k,v in pages.items():
 ii=v.get('imageinfo',[{}])[0]
 print(v.get('title'), '->', ii.get('thumburl'))
