# Canonical26: semantic error text color

Standard build and canonical check both exited 0. All 235 JavaScript assets retain exactly the canonical25 paths, bytes and SHA256 values; the existing CSP catalog passed without changes. Of 385 assets, 383 are byte-identical. The single entry CSS addition is:

```css
html:root body [class~="text-[#ff441e]"]{color:var(--yj-color-semantic-error-ink)}
```

HTML only updates that CSS filename. Full old/current inventory hashes were checked against their actual bytes and manifests; both builds are preserved in the owned review-snapshots directory.

Manifest SHA256: `725750097a463c3dc3a323b04c8b22e3650bfdc27ace60453f1c93ce2d00810c`. Source digest: `236d36286e96b4f7ad7fe5bb874528c67505c0835020b238cfe21179263bb120`. Assets total 45,317,972 bytes; largest 9,227,636 bytes; all original budgets retained.

Canonical27 was not run, per explicit instruction after the narrow CSS-only difference was verified. This is not a claim of a 26/27 reproducibility test. Runtime UI qualification remains separate; this subtask did not activate services or App.

A generic character-sequence diff helper was stopped with its normal Ctrl+C (exit 130) when it spent unnecessary time matching minified CSS; the exact prefix/suffix comparison above independently confirmed the sole inserted rule. No build was interrupted and no asset was modified.
