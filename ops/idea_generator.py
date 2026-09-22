# -- coding: utf-8 --
"""idea_generator - sinh y tuong MOI hoan toan bang Groq (YC2), ghi B.decisions."""
import sqlite3, os, json, urllib.request
from datetime import datetime
ROOT = os.getcwd()
DB = os.path.join(ROOT, 'system', 'state.db')
FM = ['shorts_fact', 'shorts_top5', 'shorts_story', 'shorts_quiz']
now = lambda: datetime.now().isoformat(timespec='seconds')
def call_groq(prompt, model='openai/gpt-oss-120b'):
    k = os.environ.get('GROQ_API_KEY', '')
    if not k:
        return None
    u = 'https://api.groq.com/openai/v1/chat/completions'
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 1.0}).encode('utf-8')
    h = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+k, 'User-Agent': 'Mozilla/5.0'}
    r = urllib.request.Request(u, data=body, headers=h)
    try:
        d = json.loads(urllib.request.urlopen(r, timeout=40).read().decode('utf-8'))
        return d['choices'][0]['message']['content']
    except Exception:
        return None
def gen_ideas(n=3):
    prompt = 'Ban la chuyen gia YouTube Shorts. Tao ' + str(n) + ' y tuong video MOI hoan toan, khac nhau, moi y 1 dong, dinh dang: topic | format | hook. Format thuoc: shorts_fact, shorts_top5, shorts_story, shorts_quiz. Tra loi tieng Viet, khong danh so.'
    out = call_groq(prompt)
    if not out:
        return []
    ideas = []
    for line in out.split(chr(10)):
        line = line.strip()
        if '|' not in line:
            continue
        p = [x.strip() for x in line.split('|')]
        if len(p) < 3:
            continue
        fmt = p[1] if p[1] in FM else FM[0]
        ideas.append((p[0], fmt, p[2]))
    return ideas[:n]
def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    chs = con.execute('SELECT id FROM channels WHERE active = 1').fetchall()
    ideas = gen_ideas(6)
    print('ideas generated:', len(ideas))
    made = 0
    for i, (topic, fmt, hook) in enumerate(ideas):
        cid = chs[i % len(chs)]['id']
        con.execute('INSERT INTO decisions (channelId, trendId, topic, format, hook, score, weightsSnapshotJson, rationale, chosenAt) VALUES (?,?,?,?,?,?,?,?,?)', (cid, None, topic, fmt, hook, 0.9, None, 'groq_idea', now()))
        made = made + 1
    con.execute('INSERT INTO changelog (version, entity, change, actor, createdAt) VALUES (?,?,?,?,?)', ('idea_generator', 'decisions', 'made=%d' % made, 'idea_generator', now()))
    con.commit()
    con.close()
    print('idea_generator done: decisions=%d' % made)
if __name__ == '__main__':
    main()
