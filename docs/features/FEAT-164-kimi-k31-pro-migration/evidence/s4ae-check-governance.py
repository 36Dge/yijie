from pathlib import Path
import subprocess,json,datetime
r=Path('/Users/jack/Downloads/Personal_Info/CrossBSD/yijie');a=r.parent/'feat164-s4ae-audit-20261027';f='docs/features/FEAT-164-kimi-k31-pro-migration';v='docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs';s='docs/dev/codex-feature-delivery/scripts/check-feature-package.sh'
commands=[('audit-claims',['node',v,'--audit-claims',f]),('strict',['bash',s,'--strict',f])]+[(f'g3-{i.lower()}',['node',v,'--gate','G3','--slice',i,f]) for i in ['S1','S2','S3','S4']]+[('g4',['bash',s,'--gate','G4',f]),('meta-lint',['pnpm','lint']),('meta-test',['pnpm','test'])]+[('shell-'+p.stem,['bash','-n',str(p.relative_to(r))]) for p in sorted((r/'scripts').glob('*.sh'))]
results=[]
for name,cmd in commands:
 start=datetime.datetime.now().astimezone().isoformat()
 with (a/(name+'.log')).open('w') as stream:
  result=subprocess.run(cmd,cwd=r,stdout=stream,stderr=subprocess.STDOUT)
 results.append({'name':name,'command':cmd,'started_at':start,'finished_at':datetime.datetime.now().astimezone().isoformat(),'exit_code':result.returncode})
 (a/'governance-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print(name,result.returncode,flush=True)
 if result.returncode:
  print((a/(name+'.log')).read_text()[-6500:]);raise SystemExit(result.returncode)
