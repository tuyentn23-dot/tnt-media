# auto_pipeline.py - render + thumbnail + upload in one command (flat)
import os, sys, json, time
sys.path.insert(0, os.getcwd())
from ops import studio_runner as SR
from ops import publish_studio as PS
from ops import os_publish as OP

def run(channel=None, kinds=None, limit=2, live=False, privacy='public'):
 _ = OP.set_channel(channel) if channel else None
 print('STEP 1 RENDER channel=' + str(channel))
 res = SR.run_batch(kinds=kinds, limit=limit)
 okn = sum(1 for r in res if r['ok'])
 print('rendered ' + str(okn) + '/' + str(len(res)))
 outs = PS.publish_manifest(privacy=privacy, limit=limit) if live else []
 msg = 'DRY-RUN skip upload' if not live else 'UPLOADED'
 print(msg)
 upl = sum(1 for o in outs if o[1])
 print('DONE uploaded ' + str(upl) + '/' + str(len(outs)))
 return {'rendered': okn, 'uploaded': upl, 'live': live}
