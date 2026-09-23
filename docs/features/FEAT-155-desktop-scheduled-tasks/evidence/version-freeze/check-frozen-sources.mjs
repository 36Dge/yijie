import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const root=path.resolve(process.argv[2]);
const contracts=path.join(root,'yijie-contracts'), desktop=path.join(root,'yijie-desktop'), host=path.join(root,'yijie-agent-host');
const {consumerSourceLock}=await import(pathToFileURL(path.join(contracts,'scripts/scheduled-consumer-source.mjs')));
const {verifyScheduledHostCandidate}=await import(pathToFileURL(path.join(desktop,'scripts/scheduled-host-build-candidate.mjs')));
for(const family of ['scheduled-plan','scheduled-execution','scheduled-draft','scheduled-task-recovery','runtime-input-only','native-turn-timing']) {
 const file=path.join(desktop,`contracts/${family}.candidate.json`);
 assert.deepEqual(consumerSourceLock(contracts,`compatibility/${family}/source.lock.json`,file,true),await readFile(file));
}
await verifyScheduledHostCandidate(desktop,contracts,host);
const temporary=await mkdtemp(path.join(tmpdir(),'feat155-source-metadata-'));
try {
 const missing=path.join(temporary,'missing-commit.json');await writeFile(missing,'{}\n');
 assert.throws(()=>consumerSourceLock(contracts,'compatibility/scheduled-plan/source.lock.json',missing,true),/Explicit committed/);
 const oldLock=JSON.parse(await readFile(path.join(desktop,'contracts/scheduled-host-build.candidate.json'),'utf8'));delete oldLock.full_commit;
 await mkdir(path.join(temporary,'contracts'));await writeFile(path.join(temporary,'contracts/scheduled-host-build.candidate.json'),JSON.stringify(oldLock));
 await assert.rejects(verifyScheduledHostCandidate(temporary,contracts,host),/identity differs/);
 console.log('PASS: six committed Contract projections, exact Host Git sources, missing commit rejection, historical-base-only rejection.');
} finally {await rm(temporary,{recursive:true,force:true});}
