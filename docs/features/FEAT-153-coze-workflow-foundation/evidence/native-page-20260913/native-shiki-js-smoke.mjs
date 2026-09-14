// Copyright 2026 Yijie contributors. Licensed under Apache-2.0.
// Normal synthetic grammar/theme compatibility, using the locked real JS engine.
// No global replacements, fault fixtures, Worker or WebAssembly engine execution.
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const shiki = path.join(root, 'bin/workflow-editor/build-workspace/node_modules/.pnpm/shiki@3.6.0/node_modules/shiki/dist');
const { createHighlighter } = await import(pathToFileURL(path.join(shiki, 'index.mjs')));
const { createJavaScriptRegexEngine } = await import(pathToFileURL(path.join(shiki, 'engine-javascript.mjs')));
const samples = {
  md: '# Workflow\n\n**Saved** text.',
  js: 'const value = "workflow";\nconsole.log(value);',
  ts: 'const value: string = "workflow";\nexport { value };',
  python: 'value = "workflow"\nprint(value)',
};
const themes = ['github-dark', 'one-dark-pro'];
const highlighter = await createHighlighter({
  langs: Object.keys(samples), themes,
  engine: createJavaScriptRegexEngine({ target: 'ES2018' }),
});
try {
  for (const [lang, code] of Object.entries(samples)) for (const theme of themes) {
    const result = highlighter.codeToTokens(code, { lang, theme });
    assert.equal(result.tokens.map(line => line.map(token => token.content).join('')).join('\n'), code);
    assert.ok(result.tokens.flat().some(token => typeof token.color === 'string' && /^#/.test(token.color)));
    const html = highlighter.codeToHtml(code, { lang, theme });
    assert.ok(html.includes('<pre'));
    assert.ok(html.includes('<span'));
    console.log(JSON.stringify({ lang, theme, lines: result.tokens.length, tokens: result.tokens.flat().length, status: 'PASS' }));
  }
} finally {
  highlighter.dispose();
}
console.log('PASS: 8 ordinary language/theme cases using original locked Shiki JavaScript engine. No global replacement, Worker, WASM engine, eval or network test execution.');
