// Copyright 2026 Yijie contributors. Licensed under Apache-2.0.
// Compile and exercise the actual pure collector with ordinary monitor states.
// No browser globals, runtime replacements, fault injection or bundle execution.
import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const require = createRequire(import.meta.url);
const ts = require(path.join(root, 'bin/workflow-editor/build-workspace/node_modules/.pnpm/typescript@5.8.2/node_modules/typescript'));
const filename = path.join(root, 'frontend/packages/workflow/playground/src/components/drag-tooltip/index.tsx');
const text = readFileSync(filename, 'utf8');
const source = ts.createSourceFile(filename, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
assert.equal(source.parseDiagnostics.length, 0);
const callbacks = [];
function visit(node) {
  if (ts.isCallExpression(node) && ts.isIdentifier(node.expression) && node.expression.text === 'useDragLayer') callbacks.push(node.arguments[0]);
  ts.forEachChild(node, visit);
}
visit(source);
assert.equal(callbacks.length, 1);
// A real compiler emits a separate owned test module; no eval/Function is used.
const result = ts.transpileModule('export const createCollector = (dragService) => (' + callbacks[0].getText(source) + ');', {
  compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 }, reportDiagnostics: true,
});
assert.equal(result.diagnostics.length, 0);
const temporary = mkdtempSync(path.join(os.tmpdir(), 'feat153-drag-collector-'));
const output = path.join(temporary, 'collector.mjs');
writeFileSync(output, result.outputText);
const { createCollector } = await import(pathToFileURL(output));
let currentItem = null, currentOffset = null, seen;
const monitor = {
  getItem: () => currentItem,
  getItemType: () => currentItem ? 'workflow-node' : null,
  getSourceClientOffset: () => currentOffset,
};
const collect = createCollector({ computeCanDrop: parameters => {
  seen = parameters;
  return { allowDrop: Boolean(parameters.dragNode.type), message: parameters.dragNode.type ? '可以放置' : undefined };
} });
const initial = collect(monitor);
assert.deepEqual(initial.currentOffset, { x: 0, y: 0 });
assert.equal(initial.allowDrop, false);
assert.equal(initial.item, null);
console.log('PASS: first synchronous collection with no dragged node');
currentItem = { nodeType: '15', nodeJson: { id: 'synthetic-text' } };
currentOffset = { x: 120, y: 240 };
const dragging = collect(monitor);
assert.equal(dragging.item, currentItem);
assert.equal(dragging.currentOffset, currentOffset);
assert.equal(seen.coord, currentOffset);
assert.equal(seen.dragNode.json, currentItem.nodeJson);
assert.equal(dragging.allowDrop, true);
console.log('PASS: item and coordinates use the same current monitor snapshot');
currentOffset = { x: 300, y: 160 };
assert.equal(collect(monitor).currentOffset, currentOffset);
assert.equal(seen.coord, currentOffset);
console.log('PASS: subsequent synchronous collection reads updated coordinates');
console.log(JSON.stringify({ collectorSource: filename, compiledTestModule: output, cases: 3, qualification: 'pure collector only; actual React DnD App qualification remains separate' }));
