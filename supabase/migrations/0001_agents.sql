create table if not exists agents (
  slug text primary key,
  name text not null,
  role text,
  description_md text not null,
  order_index int default 0,
  source_sha text,
  updated_at timestamptz default now()
);

create table if not exists agent_proposals (
  id uuid primary key default gen_random_uuid(),
  agent_slug text references agents(slug) on delete cascade,
  proposal_type text check (proposal_type in ('modification','addition')),
  body_md text not null,
  author text,
  status text default 'open',
  created_at timestamptz default now()
);

-- RLS
alter table agents enable row level security;
alter table agent_proposals enable row level security;

create policy "agents are publicly readable"
  on agents for select using (true);

create policy "proposals are publicly readable"
  on agent_proposals for select using (true);

create policy "anyone can submit proposals"
  on agent_proposals for insert with check (true);

-- Service role bypasses RLS, so the sync script can still write to `agents`.
