import sys, os, json, traceback
sys.path.insert(0, os.getcwd())
res = []
def L(m):
 res.append(str(m))
 open('output/_bt.txt', 'w', encoding='utf-8').write(chr(10).join(res))
try:
 from ops import channel_style as cs
 from ops import publish_engine as pe
 ch = 'Mialinhcute'
 item = {'id': 'bt1', 'hook': 'Test build then upload', 'body': 'noi dung test', 'payoff': 'ket thuc', 'topic': 'cat'}
 out = os.path.join(os.getcwd(), 'output', 'bt1.mp4')
 L('building...')
 cs.build_styled(item, out)
 L('built size=' + str(os.path.getsize(out)))
 L('publishing...')
 resp = pe.publish(out, ch, item)
 L('resp_none=' + str(resp is None))
 if resp:
 L('VIDEO_ID=' + str(resp.get('id')))
 s = json.load(open(pe.STATE, encoding='utf-8'))
 L('state_total=' + str(len(s.get('publishes', {}))))
 L('bt1_recorded=' + str('bt1' in s.get('publishes', {})))
except Exception:
 L('ERR ' + traceback.format_exc()[-800:])
