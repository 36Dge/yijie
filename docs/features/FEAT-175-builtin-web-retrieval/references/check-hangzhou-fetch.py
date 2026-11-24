"""Run one isolated weather regression through Host, Runtime, PostgreSQL and the desktop view."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import re
import sys
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[5]

def wait_file(path, owner):
    deadline=time.monotonic()+60
    while time.monotonic()<deadline:
        if path.is_file(): return
        if owner.poll() is not None: raise RuntimeError(f'{path.name} owner exited ({owner.returncode})')
        time.sleep(.2)
    raise TimeoutError(f'waiting for {path.name}')

def check_daily_forecast(answer, source):
    page=source['fetches'][0]['body']
    result={}
    parts=re.split(r'- ## (2[3-9])日[^\n]*\n',page['markdown'].partition('_分时段预报_')[0])
    for pos in range(1,len(parts),2):
        day=parts[pos]
        weather=next(line.strip() for line in parts[pos+1].splitlines() if line.strip())
        temperatures=re.findall(r'(\d+)℃',parts[pos+1])
        date=re.compile(r'(?<![0-9])(?:11[月./-])?'+day+r'(?:日|(?=[\s|（(/.-]))')
        matching=[line for line in answer.splitlines() if date.search(line)]
        covered=any(weather in line and all(re.search(r'(?<![0-9])'+t+r'(?![0-9])',date.sub('',line,count=1)) for t in temperatures) for line in matching)
        result[day]=covered
    if len(result)!=7 or not all(result.values()) or page['url'] not in answer:
        raise AssertionError(f'Compare final answer with recorded dates, conditions, temperatures and source: {result}')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--recording',type=Path,required=True)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--kimi-key-file',type=Path)
    p.add_argument('--allowance-directory',type=Path)
    args=p.parse_args()
    if not os.environ.get('FEAT175_TEST_DATABASE_URL'):p.error('an isolated loopback FEAT-175 PostgreSQL is required')
    if args.kimi_key_file and not args.allowance_directory:p.error('supply the shared authorization ledger')
    directory=args.directory.resolve()
    directory.mkdir(mode=0o700,parents=True,exist_ok=False)
    runtime=ROOT/'yijie-codex/.yijie/build/native-skill-marketplace-v1'
    artifact=runtime/json.loads((runtime/'current.json').read_text())['artifact']
    env=dict(os.environ,HANGZHOU_REPLAY_DIRECTORY=str(directory),
             FEAT175_PRODUCT_WORKER_MANIFEST=str(ROOT/'yijie-connectors/bin/market-worker/current.json'),
             YIJIE_CODEX_INTEGRATION_BINARY=str(artifact/'codex'),
             YIJIE_CODEX_INTEGRATION_MANIFEST=str(artifact/'runtime-manifest.json'))
    provider_cmd=[sys.executable,'-B',str(Path(__file__).with_name('replay-hangzhou-fetch.py')),
                  '--recording',str(args.recording.resolve()),'--directory',str(directory)]
    if args.kimi_key_file:
        provider_cmd.extend(['--kimi-key-file',str(args.kimi_key_file.resolve()),'--allowance-directory',str(args.allowance_directory.resolve())])
    api=None
    api_status=None
    def run(project,cmd,log):
        with (directory/log).open('w') as stream:
            subprocess.run(cmd,cwd=ROOT/project,env=env,stdout=stream,stderr=subprocess.STDOUT,check=True)
    with (directory/'provider.log').open('w') as model_log,(directory/'api.log').open('w') as api_log:
        provider=subprocess.Popen(provider_cmd,cwd=ROOT,stdout=model_log,stderr=subprocess.STDOUT)
        try:
            wait_file(directory/'provider-url',provider)
            env['HANGZHOU_REPLAY_MODEL']=(directory/'provider-url').read_text()
            api=subprocess.Popen(['go','test','-timeout','50m','-count=1','-v','./internal/modules/webretrieval/interfaces/http','-run','^TestHangzhouRecordedPageOperations$'],cwd=ROOT/'yijie-api',env=dict(env,HANGZHOU_REPLAY_SERVE='1'),stdout=api_log,stderr=subprocess.STDOUT)
            wait_file(directory/'test-grant.json',api)
            run('yijie-agent-host',['go','test','-count=1','-v','-run','^TestHangzhouRecordedFetchTurn$','./internal/codex'],'host.log')
            run('yijie-agent-host',['go','test','-count=1','-v','-run','^TestProjectHangzhouFetchTurn$','./internal/session'],'host-projection.log')
            env.update(YIJIE_FEAT132_TEST_EXCHANGE=str(directory/'native-exchange.json'),YIJIE_FEAT132_TEST_VIEW_OUTPUT=str(directory/'saved-view.json'),
                       CARGO_TARGET_DIR=str(ROOT/'yijie-desktop/.local/development/target'))
            run('yijie-desktop',['cargo','test','--offline','--locked','--manifest-path','src-tauri/Cargo.toml','--lib','chat::database::tests::recorded_hangzhou_fetch_turn_reopens_with_final_answer','--','--ignored','--exact'],'native.log')
            env.update(HANGZHOU_RENDER_DIRECTORY=str(directory))
            for fname in ['saved-view.live.json','saved-view.json']:
                env['HANGZHOU_RENDER_FILE']=fname
                run('yijie-desktop',['pnpm','exec','vitest','run','src/components/chat/ChatRepeatedCommentary.test.ts'],fname+'.log')
        finally:
            if api is not None:
                (directory/'finish-api').touch()
                api_status=api.wait(timeout=30)
            if (directory/'provider-url').exists():
                close=(directory/'provider-url').read_text().removesuffix('/v1')+'/close'
                with urlopen(Request(close,data=b'',method='POST'),timeout=5): pass
            provider_status=provider.wait(timeout=30)
    if api_status!=0 or provider_status!=0:
        raise RuntimeError(f'Fixture did not complete normally (API {api_status}, model peer {provider_status})')
    outcome=json.loads((directory/'completed-turn-metrics.json').read_text())
    outcome['pageReadsAtReceiver']=json.loads((directory/'recorded-http-reads.json').read_text())[outcome['scope']]
    assert outcome['pageReadsAtReceiver']==1 and outcome['status']=='completed'
    outcome['sampling']=json.loads((directory/'sampling.json').read_text())
    if args.kimi_key_file:
        final=(directory/'final-answer.md').read_text().strip()
        digest=hashlib.sha256(final.encode()).hexdigest()
        receipt=next((json.loads(f.read_text()) for f in directory.glob('kimi-receipt-*.json') if digest in json.loads(f.read_text())['publicTexts']),None)
        assert receipt and receipt.get('status')==200 and receipt.get('completed'), 'desktop final does not match a real Kimi response'
        outcome['kimiResponse']=receipt['responseId']
        outcome['finalSha256']=digest
        outcome['forecastDays']=check_daily_forecast(final,json.loads((directory/'source.json').read_text()))
    for name,file in [('live','saved-view.live.json'),('reopened','saved-view.json')]:
        outcome[name]=json.loads((directory/(file+'.render.json')).read_text())
        assert all(r['visibleRepeatedText']==1 and r['visibleFinals']==1 for r in outcome[name])
    (directory/'verification.json').write_text(json.dumps(outcome,ensure_ascii=False,indent=2))
    print(directory/'verification.json')

if __name__=='__main__': main()
