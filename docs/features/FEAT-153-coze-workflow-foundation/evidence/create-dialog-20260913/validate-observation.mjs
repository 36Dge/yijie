import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
const root = path.resolve(process.cwd(), 'yijie-contracts');
const require = createRequire(path.join(root, 'package.json'));
const Ajv = require('ajv/dist/2020.js').default;
const baseline = '32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4';
const sources = [JSON.parse(execFileSync('git', ['show', `${baseline}:sdks/jsonschema/workflow-local.schema.json`], { cwd: root, encoding: 'utf8' })), JSON.parse(readFileSync(path.join(root, 'sdks/jsonschema/workflow-local.schema.json')))];
for (const filename of process.argv.slice(2)) {
 const observation = JSON.parse(readFileSync(filename));
 for (const [index, key] of ['legacy', 'metadata'].entries()) {
  const schema = sources[index], ajv = new Ajv({ strict: true, strictRequired: false });
  ajv.addKeyword({ keyword: 'x-utf8-max-bytes', type: 'string', schemaType: 'number', validate: (n,v) => Buffer.byteLength(v,'utf8') <= n });
  for (const key of ['x-operation-required', 'x-operation-field', 'x-operation-restrict-fields', 'x-operation-optional']) ajv.addKeyword(key);
  ajv.addSchema(schema);
  const validate = ajv.compile({ $ref: `${schema.$id}#/$defs/${observation.path.includes('?') ? 'WorkflowList' : 'Workflow'}` });
  if (!validate(observation[key])) throw new Error(`${key} schema failed: ${JSON.stringify(validate.errors)}`);
 }
 console.log(`${path.basename(filename)}: baseline reader and new reader accepted actual responses`);
}
