import assert from "node:assert/strict";
import test from "node:test";
import { loadManifest } from "../scripts/repo-manifest.mjs";

test("repository manifest contains eleven owned children with the explicit Coze main branch", async () => {
  const manifest = await loadManifest();
  assert.equal(manifest.repos.length, 11);
  assert.equal(new Set(manifest.repos.map((repo) => repo.name)).size, 11);
  const coze = manifest.repos.find((repo) => repo.name === "yijie-coze");
  assert.deepEqual(coze, {
    name: "yijie-coze",
    path: "../yijie-coze",
    url: "https://github.com/36Dge/yijie-coze.git",
    branch: "main",
    type: "workflow-engine",
    owner: "backend-team",
  });
  assert.ok(manifest.repos.filter((repo) => repo !== coze)
    .every((repo) => repo.branch === "develop" && repo.url.startsWith("https://github.com/36Dge/")));
});
