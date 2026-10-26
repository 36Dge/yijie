from pathlib import Path
import subprocess,json,datetime
R=Path('/Users/jack/Downloads/Personal_Info/CrossBSD/yijie');A=R.parent/'feat164-s4af-audit-20261027';F='docs/features/FEAT-164-kimi-k31-pro-migration';V='docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs';S='docs/dev/codex-feature-delivery/scripts/check-feature-package.sh'
commands=[('audit-claims',['node',V,'--audit-claims',F]),('strict',['bash',S,'--strict',F]),('g3-s4',['node',V,'--gate','G3','--slice','S4',F]),('g4-expected-block',['node',V,'--gate','G4',F]),('meta-lint',['pnpm','lint']),('meta-test',['pnpm','test'])]+[('shell-'+p.stem,['bash','-n',str(p.relative_to(R))]) for p in sorted((R/'scripts').glob('*.sh'))]
results=[]
for name,cmd in commands:
 at=datetime.datetime.now().astimezone().isoformat()
 with (A/(name+'.log')).open('w') as log:proc=subprocess.run(cmd,cwd=R,stdout=log,stderr=subprocess.STDOUT)
 out=(A/(name+'.log')).read_text();expected=name=='g4-expected-block';errors=[x for x in out.splitlines() if x.startswith('ERROR:')]
 accepted=(proc.returncode==0) if not expected else (proc.returncode==1 and len(errors)==1 and 'G4' in errors[0] and 'pass' in errors[0])
 results.append({'name':name,'command':cmd,'started_at':at,'finished_at':datetime.datetime.now().astimezone().isoformat(),'exit_code':proc.returncode,'result':('EXPECTED_BLOCK' if expected else 'PASS') if accepted else 'UNEXPECTED_FAILURE'})
 (A/'governance-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print(name,proc.returncode,results[-1]['result'],flush=True)
 if not accepted:print(out[-5000:]);raise SystemExit(1)
