p='auto_youtube_bot_v2.py'
s=open(p,encoding='utf-8').read()
i=s.find('mp3s =')
j=s.find(chr(10), i)
old=s[i:j]
print('OLD=', repr(old))
new='mp3s = []'+chr(10)+chr(9)+chr(9)+'if mdir.exists():'+chr(10)+chr(9)+chr(9)+chr(9)+'mp3s = list(mdir.glob(''.mp3'')) + list(mdir.glob(''.wav''))'
s=s[:i]+new+s[j:]
open(p,'w',encoding='utf-8').write(s)
print('NEW HAS WAV:', '*.wav' in s)
