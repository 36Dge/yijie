import os,sys,subprocess
from pathlib import Path
root=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');q=root/'feat164-qualification-20261025';desktop=q/'yijie-desktop'
env={k:os.environ[k] for k in ('PATH','HOME','TMPDIR','CARGO_HOME','RUSTUP_HOME','SDKROOT','DEVELOPER_DIR','PKG_CONFIG_PATH') if k in os.environ}
env.update(YIJIE_KIMI_K31_CALL_SURFACES='media',YIJIE_DEMO_FAST_PROVIDER_KEY_FILE=str(desktop/'.local/feat164-s4c-fixture/minimax'),YIJIE_KIMI_API_KEY_FILE=str(desktop/'.local/feat164-s4c-fixture/kimi'),YIJIE_PERMISSION_VERIFICATION_BASE_URL='http://127.0.0.1:18083/v1',CARGO_NET_OFFLINE='true',YIJIE_WORKER_TARGET_DIR=str(root/'feat164-s4b-worker-build-20261025/target'),YIJIE_KIMI_K31_EXECUTION_PAUSED='true' if sys.argv[1]=='paused' else 'false')
command=['bash','scripts/run-local-demo-fast.sh','--packaged','--kimi-k31-pro', '--prepare-only' if sys.argv[1]=='build' else '--reopen']
raise SystemExit(subprocess.run(command,cwd=desktop,env=env).returncode)
