// Sync agent definitions from .claude/agents/*.md to Supabase.
//
// Mapping (markdown frontmatter → Supabase `agents` columns):
//   name          (kebab-case identifier; required by Claude Code subagent runtime)
//                 → slug                (primary key)
//   display_name  (human-readable)
//                 → name
//   description   (one-line role / Claude Code invocation hint)
//                 → role
//   order         (council ordering)
//                 → order_index
//   body markdown (everything after frontmatter)
//                 → description_md
//   env GIT_SHA   → source_sha
//
// Runs in CI via .github/workflows/sync-agents.yml on pushes to main that
// touch .claude/agents/**, README.md, or this script. Also runnable locally
// (`npm run sync`) with the required env vars set.

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';
import { createClient } from '@supabase/supabase-js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');
const AGENTS_DIR = path.join(REPO_ROOT, '.claude', 'agents');

const { SUPABASE_URL, SUPABASE_SERVICE_KEY, GIT_SHA } = process.env;

if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY) {
  console.error('FATAL: SUPABASE_URL and SUPABASE_SERVICE_KEY must both be set.');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY, {
  auth: { autoRefreshToken: false, persistSession: false },
});

const warnings = [];

// --------- collect files ---------
let entries;
try {
  entries = await fs.readdir(AGENTS_DIR, { withFileTypes: true });
} catch (err) {
  console.error(`FATAL: cannot read ${AGENTS_DIR}: ${err.message}`);
  process.exit(1);
}

const mdFiles = entries
  .filter((e) => e.isFile() && e.name.endsWith('.md'))
  .map((e) => path.join(AGENTS_DIR, e.name))
  .sort();

if (mdFiles.length === 0) {
  console.error(`FATAL: no agent files found in ${AGENTS_DIR}. Refusing to sync — this would delete every row in 'agents'.`);
  process.exit(1);
}

// --------- parse + build rows ---------
const rows = [];

for (const filePath of mdFiles) {
  const base = path.basename(filePath);
  const raw = await fs.readFile(filePath, 'utf8');
  const parsed = matter(raw);
  const fm = parsed.data || {};
  const body = (parsed.content || '').trim();

  const slug = fm.name; // existing `name:` is the kebab-case slug
  const displayName = fm.display_name;
  const role = fm.description;
  const order = typeof fm.order === 'number' ? fm.order : 0;

  if (!slug) {
    warnings.push(`${base}: missing \`name:\` in frontmatter; skipping.`);
    continue;
  }
  if (!displayName) {
    warnings.push(`${base}: missing \`display_name:\`; falling back to slug.`);
  }
  if (!role) {
    warnings.push(`${base}: missing \`description:\` (role); leaving role NULL.`);
  }
  if (typeof fm.order !== 'number') {
    warnings.push(`${base}: missing or non-numeric \`order:\`; defaulting to 0.`);
  }
  if (!body) {
    warnings.push(`${base}: empty body after frontmatter; description_md will be empty.`);
  }

  rows.push({
    slug,
    name: displayName || slug,
    role: role || null,
    description_md: body,
    order_index: order,
    source_sha: GIT_SHA || null,
    updated_at: new Date().toISOString(),
  });
}

if (rows.length === 0) {
  console.error('FATAL: parsed 0 valid agent rows. Refusing to sync.');
  process.exit(1);
}

// --------- upsert ---------
const { error: upsertErr } = await supabase
  .from('agents')
  .upsert(rows, { onConflict: 'slug' });

if (upsertErr) {
  console.error('FATAL: upsert failed:', upsertErr);
  process.exit(1);
}

// --------- delete stale rows ---------
const slugList = `(${rows.map((r) => r.slug).join(',')})`;
const { error: deleteErr, count: deletedCount } = await supabase
  .from('agents')
  .delete({ count: 'exact' })
  .not('slug', 'in', slugList);

if (deleteErr) {
  console.error('FATAL: stale-row delete failed:', deleteErr);
  process.exit(1);
}

// --------- summary ---------
console.log('');
console.log('=== Agent sync summary ===');
console.log(`Upserted: ${rows.length}`);
console.log(`Deleted:  ${deletedCount ?? 0}`);
if (GIT_SHA) console.log(`source_sha: ${GIT_SHA}`);
if (warnings.length > 0) {
  console.log('');
  console.log(`Warnings (${warnings.length}):`);
  for (const w of warnings) console.log(`  - ${w}`);
}
console.log('');
