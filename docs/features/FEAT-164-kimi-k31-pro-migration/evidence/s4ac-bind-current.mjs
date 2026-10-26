import fs from 'node:fs';
import {createRequire} from 'node:module';
const b='/Users/jack/Downloads/Personal_Info/CrossBSD',a=b+'/feat164-s4ac-audit-20261027',f=b+'/yijie/docs/features/FEAT-164-kimi-k31-pro-migration/feature.yaml';
const YAML=createRequire(b+'/yijie/package.json')('yaml');let source=fs.readFileSync(f,'utf8'),d=YAML.parse(source);
const binding=JSON.parse(fs.readFileSync(a+'/source-evidence-binding.json')),protection=JSON.parse(fs.readFileSync(a+'/preservation.json')),daily=JSON.parse(fs.readFileSync(a+'/daily-build-audit.json'));
if(binding.status!=='PASS'||protection.result!=='PASS'||daily.result!=='PASS_PREPARE_ONLY')throw Error('Evidence incomplete');
const commits=['yijie-desktop','yijie-agent-host','yijie-contracts','yijie-codex','yijie-connectors'].map(repository=>({repository,full_sha:binding.source_commits[repository].head}));
const now=protection.at,env='macOS aarch64; ea8763d product equals actual c98 App179dbd; Host4f966e8 / Contracts c5d1383 / Runtime11fd-r5 / Connectorscc56 / Skills595; historical runs retain original source and time';
const s=d.slices.find(s=>s.id==='S4');s.commits=commits;
const allCommits=[...new Map([...d.slices.filter(x=>x.id!=='S4').flatMap(x=>x.commits),...commits].map(x=>[x.repository+'@'+x.full_sha,x])).values()];
s.freshness={...s.freshness,commits:allCommits,verified_at:now};
for(const field of ['local_evidence','boundary_evidence','vertical_evidence']){
 const v=s[field];v.command=field==='local_evidence'?'python3 feat164-s4ac-audit-20261027/run-checks.py':field==='boundary_evidence'?'python3 feat164-s4ac-audit-20261027/audit-bindings.py':'Canonical S4AA same-build reopen via launch.py + CUA business-state observation + normal Cmd-Q + stopped-copy read-only audit';v.environment=env;v.verified_at=now;v.refs=['08-verification-report.md#E164-S4AC-BINDING','08-verification-report.md#E164-S4AC-FINAL'];
}
s.local_evidence.reason='当前22前端、38Host（含子测试）、33Native、5计划、3daily profile、19来源全部通过；48 retained Runtime证据逐hash保留，未重跑旧38次loopback。';
s.boundary_evidence.reason='501项旧证据SHA一致、310业务文件相同；51日常维护/identity由其专属四矩阵及当前回归支持，54 Host URL筛选由专属来源证据支持；53真实图片/工具/搜索传输及本轮当前App历史重开绑定，来源差异未隐去。';
s.vertical_evidence.reason='当前App菜单/旧线程中断继续/关闭计划/图片工具/18来源partial及正常退出通过；完整unknown/never-sent App操作链仍未在当前资格库自然观察。仅此完整范围NOT RUN，不再列供应商非文本缺口；不造故障，不将组件状态测试冒充完整App。';
s.status_reason='来源绑定、安全状态和当前App可达子集已收口；完整TCONF04/core/业务状态还缺安全可达的unknown/never-sent App链，S4仍pending。日常prepare-only已通过，不等于日常激活。';
const temporal=d.temporal_contract_matrix.executable_tests.find(t=>t.slice_id==='S4');temporal.command='python3 feat164-s4ac-audit-20261027/run-checks.py + audit-bindings.py + canonical same-build App observed subset';temporal.verified_at=now;temporal.commits=allCommits;temporal.evidence_ref='08-verification-report.md#E164-S4AC-BINDING';temporal.command_note='当前来源与安全状态/实际App子集PASS；完整unknown/never-sent App链仍NOT RUN，保留完整TCONF04 pending；搜索答案质量OWNER_EXCLUDED。';
for(const [key,v] of Object.entries(d.final_e2e)){
 v.command='Canonical same-build App reopen/CUA + normal Cmd-Q exit0 + snapshot-stopped.py + read_sqlcipher.py retained-copy audit';v.environment=env;v.verified_at=now;v.commits=commits;v.evidence_refs=['08-verification-report.md#E164-S4AC-FINAL'];v.historical_binding_note='此前原S4V判定与真实请求来源保留；本条为当前S4AC零模型历史重开/状态/正常退出审计，不把旧运行改称本轮。';
 if(key==='teardown')v.reason='当前实际c98/Host4f/r5 App正常退出exit0、无进程/句柄和补发，四Runtime库WAL0/integrity、71表旧行保持；原unknown不清除，日常App未启动。';
 else v.reason='当前源与当前App安全可达业务子集通过，完整unknown/never-sent App操作链仍未自然观察；53真实图片/工具/搜索传输与54来源显示已绑定，不再是缺口。搜索答案质量与亮暗/键盘/最小窗口排除，不计PASS、不延期。';
}
for(const key of ['slices','temporal_contract_matrix','final_e2e']){
 const re=new RegExp(`^${key}:\\n[\\s\\S]*?(?=^[A-Za-z_][A-Za-z0-9_]*:|$(?![\\s\\S]))`,'m');source=source.replace(re,()=>YAML.stringify({[key]:d[key]},{lineWidth:120})+'\n');
}
YAML.parse(source);fs.writeFileSync(f,source);console.log('S4 current-source binding and final scoped verdicts updated; no full gate promotion.');
