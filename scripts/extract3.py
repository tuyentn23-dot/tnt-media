import requests, re
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://support.google.com/youtube/answer/11914225', timeout=15, headers=h)
txt = re.sub('<script[^>]>.?</script>', ' ', r.text, flags=re.S)
txt = re.sub('<[^>]+>', ' ', txt)
txt = re.sub(' +', ' ', txt)
i = txt.find('viewers are matched')
print(txt[i:i+1500].encode('ascii', 'replace').decode())
