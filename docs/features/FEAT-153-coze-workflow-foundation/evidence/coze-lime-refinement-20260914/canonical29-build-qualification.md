# Canonical29 native workflow avatar refinement

Standard build and check both exited 0. All 235 JavaScript paths, bytes and SHA256 values are identical to preserved canonical28. 383 of 385 assets are byte-identical. The entry CSS adds only the approved native workflow avatar transparent background/border rule; HTML only updates the entry CSS filename.

The real minified addition is:

```css
html:root body .coz-avatar.coz-avatar-platform:has([data-icon-kind=workflow]){background:0 0;border-color:#0000}
```

The existing exact CSP catalog passed unchanged. No additional AST scan, broad test rerun or canonical30 build was needed or claimed. The built assets were not modified.

Manifest SHA256: `2a2fa3d5ac83d50994970b8ba62077f7743366aab8b683da171761e06e0b2a44`. Source digest: `8ccbc99c0529a85dc93e9694d53b1b51e9c441bd54af52c5fc19cd4ea052a689`. Assets total 45,316,202 bytes; largest 9,227,636 bytes, within all original budgets. Original dependency lock/build configuration and runtime CSP permissions remain unchanged.

Canonical28 and29 actual output snapshots are preserved. This subtask did not activate services or the App; the avatar's visual appearance remains an actual App check.
