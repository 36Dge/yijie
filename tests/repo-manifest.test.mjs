import assert from "node:assert/strict";
import test from "node:test";
import { loadManifest } from "../scripts/repo-manifest.mjs";

test("repository manifest contains the ten child repositories", async () => {
  const manifest = await loadManifest();
  assert.equal(manifest.repos.length, 10);
  assert.equal(new Set(manifest.repos.map((repo) => repo.name)).size, 10);
  assert.ok(manifest.repos.every((repo) => repo.branch === "develop"));
});
