P='tools/_mk_song2_video.py'
s=open(P,encoding='utf-8').read()
old="""            t=l.split('Duration:')[1].split(',')[0].strip()
            h,m,s=t.split(':')
            return int(h)*3600+int(m)*60+float(s)"""
new="""            t=l.split('Duration:')[1].split(',')[0].strip()
            parts=t.split(':')
            if len(parts)==3:
                h,m,s=parts
                return int(h)*3600+int(m)*60+float(s)
            elif len(parts)==2:
                m,s=parts
                return int(m)*60+float(s)"""
print('found:', old in s)
s=s.replace(old,new,1)
open(P,'w',encoding='utf-8').write(s)
print('fixed')
