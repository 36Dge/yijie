# Canonical27 lime refinement: precise incremental review

Compared preserved canonical26 actual bytes with standard canonical27 output. 379 of 385 assets retain their exact paths, bytes and SHA256. Changes are two CSS files, three JavaScript files and the entry HTML. Total assets: 45,316,090 bytes; largest: 9,227,636 bytes; the original file/total/per-file budgets remain unchanged.

The complete changed JavaScript bytes have exactly these differences:

- Original NodeIconOutlined module869951 changes its CSS boxShadow template to honor the optional native outline variable. All other original native modules are unchanged.
- The existing TypeScript worker runtime changes only the standard Rspack build fullhash.
- The entry script changes only its standard build fullhash and three manifest-relative asset contenthash references.

`canonical26-27-js-exact-delta.json` verifies whole-file identity after only these reviewed replacements in memory. No output file was modified or normalized. Actual old/new outputs remain preserved in owned review-snapshots directories.

The existing TypeScript AST and alias audit ran only on these three changed scripts. It found the same eight existing sites: two global-object Function fallbacks, one original worker importScripts loader, one original page chunk loader, and four knowledge/image fetch helpers in unchanged module factories. Existing conditions and current local-scope reachability remain unchanged. This does not grant runtime permission: worker-src none, connect-src none, and script-src self without unsafe-eval or wasm-unsafe-eval remain enforced. No worker, WASM, eval, network or bundle code was executed by the audit.

The 45-entry exact-byte review catalog updates only these three files; the other42 entries were checked against unchanged actual bytes. Three focused catalog tests passed. Canonical27 stopped at the expected missing-new-hash gate; canonical28 is required to produce a manifest through normal build and check after this review metadata update. Frozen product source/dependencies/build configuration are identical between27/28; the catalog itself changes the full source digest.

The paired compiler gate reports126 unchanged original upstream diagnostics and zero new/modified-source diagnostics. This does not claim upstream is type-error-free. Runtime color-mix parsing and visual result are reserved for actual App qualification. No App or service was started here.
