#!/usr/bin/env node
// Read-only verification of actual qualification wire using the canonical schema.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync, writeFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';

const [workspace, run] = process.argv.slice(2).map(value => path.resolve(value));
assert.ok(workspace && run, 'workspace and run directory are required');
const contracts = path.join(workspace, 'yijie-contracts');
const require = createRequire(path.join(contracts, 'package.json'));
const Ajv = require('ajv/dist/2020.js').default;
const load = file => JSON.parse(readFileSync(file, 'utf8'));
const sha = file => createHash('sha256').update(readFileSync(file)).digest('hex');
const schemaFile = path.join(contracts, 'sdks/jsonschema/market-broker-control.schema.json');
const schema = load(schemaFile);
const manifest = load(path.join(contracts, 'compatibility/market-broker-control/control.json'));
const ajv = new Ajv({strict: true, allErrors: true});
ajv.addFormat('uuid', /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i);
ajv.addSchema(schema);
const validate = (name, value) => {
  const check = ajv.getSchema(`${schema.$id}#/$defs/${name}`);
  assert.ok(check(value), `${name}: ${JSON.stringify(check.errors)}`);
};
const result = load(path.join(run, 'result.json'));
assert.equal(result.status, 'COMPLETED_OBSERVATIONS');
assert.equal(result.external_calls, 0);
assert.equal(result.real_model_calls, 0);
assert.equal(result.platform_credentials_read_or_written, 0);
assert.equal(result.internal_capability_in_observed_wire, false);
assert.deepEqual(result.internal_capability_in_temporary_files, []);
assert.equal(result.temporary_data_removed_after_exit, true);
for (const exit of Object.values(result.normal_shutdown)) {
  assert.equal(exit.normal_eof, true);
  assert.equal(exit.exit_code, 0);
}
assert.equal(result.local_responses_requests, 4);
assert.equal(result.cases.length, 2);
assert.equal(result.cases[0].firstTurn, true);
assert.equal(result.cases[1].firstTurn, false);
assert.equal(result.cases[0].threadId, result.cases[1].threadId);
assert.notEqual(result.cases[0].turnId, result.cases[1].turnId);
assert.notEqual(result.cases[0].binding.capabilityRef, result.cases[1].binding.capabilityRef);
for (const [index, item] of result.cases.entries()) {
  assert.equal(item.callbacks.length, 1);
  assert.equal(item.callFinal.state, index === 0 ? 'consumed' : 'rejected');
  assert.equal(item.nativeTool.status, index === 0 ? 'completed' : 'failed');
  assert.equal(item.revoked.state, 'revoked');
  assert.equal(item.reprepare.code, 'lease_revoked');
  assert.equal(item.callFinal.identity.nativeThreadId, item.threadId);
  assert.equal(item.callFinal.identity.nativeTurnId, item.turnId);
  validate('ElicitationMetadata', item.callbacks[0].request.params._meta);
}
const lines = readFileSync(path.join(run, 'wire.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
const requests = new Map();
let controlFrames = 0;
for (const record of lines) {
  if (record.kind === 'broker_control_request') {
    const command = manifest.commands.find(value => value.method === record.data.method);
    assert.ok(command);
    validate(command.request, record.data);
    requests.set(record.data.requestId, command);
    controlFrames += 1;
  } else if (record.kind === 'broker_control_response') {
    const command = requests.get(record.data.requestId);
    assert.ok(command, 'response must follow its own request');
    validate(Object.hasOwn(record.data, 'code') ? 'Error' : command.response, record.data);
    requests.delete(record.data.requestId);
    controlFrames += 1;
  }
}
assert.equal(requests.size, 0);
const verification = {
  status: 'PASS', control_frames: controlFrames, actual_native_turns: 2,
  actual_gateway_elicitations: 2, admitted_synthetic_lookup: 1, rejected_synthetic_lookup: 1,
  evidence_only_not_product_D4: true,
  result_sha256: sha(path.join(run, 'result.json')), wire_sha256: sha(path.join(run, 'wire.jsonl')),
  source_schema_sha256: sha(schemaFile),
};
writeFileSync(path.join(run, 'verification.json'), `${JSON.stringify(verification, null, 2)}\n`);
console.log(JSON.stringify(verification));
