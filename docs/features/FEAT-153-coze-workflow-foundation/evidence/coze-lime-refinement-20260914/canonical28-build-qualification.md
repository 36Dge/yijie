# Canonical28 build qualification

Standard canonical28 build and check both exited 0. All 385 asset paths, byte lengths and SHA256 values exactly match the actual canonical27 output. The product source, dependency lock and build configuration stayed frozen; only the explicit three-file CSP review catalog metadata changed between these builds.

- Manifest SHA256: `6cf9228ae89480f94197ff48193fdaa0e0580a65cae893ae8c93001489b12def`
- Source digest: `b69117dec6ff31092f6078dad3281d5ca73270042f2e6ebf05a43dd5cebe1fdf`
- Asset total: 45,316,090 bytes; largest: 9,227,636 bytes; original budgets unchanged.
- Paired typecheck:126 unchanged original diagnostics; zero new/modified source diagnostics.
- Exact catalog tests:3 passed; existing runtime CSP unchanged.

Canonical27/28 actual outputs are preserved in owned build review-snapshots. This result qualifies the reproducible bundle and controlled static resource gate; actual App appearance, including color-mix support, remains a separate UI check. This subtask did not activate any service or App.
