"""Authorized native AX resizing and unedited window capture of the owned App."""
import json,subprocess,sys,time
from pathlib import Path
pid,width,height,filename=sys.argv[1:]
subprocess.run(['/tmp/feat153-followup-window-observer-v3',pid,width,height],check=True,stdout=subprocess.DEVNULL)
time.sleep(.35)
rows=json.loads(subprocess.check_output(['/tmp/feat153-followup-window-observer-v2',pid],text=True))
w=max(rows,key=lambda x:x['bounds']['Width']*x['bounds']['Height'])
assert w['bounds']['Width']==int(width) and w['bounds']['Height']==int(height),w
subprocess.run(['/usr/sbin/screencapture','-x','-o','-l',str(w['window_id']),filename],check=True)
Path(filename+'.json').write_text(json.dumps(w,indent=2)+'\n')
print(json.dumps(w))
