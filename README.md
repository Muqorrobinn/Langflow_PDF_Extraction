# Langflow_PDF_Extraction
Make a flow of AI automation use Langflow

create table public.paper_reviews (
  id uuid not null default gen_random_uuid (),
  created_at timestamp with time zone not null default timezone ('utc'::text, now()),
  metadata jsonb not null,
  problem_statement text not null,
  novelty text not null,
  methodology jsonb not null,
  key_metrics text not null,
  limitations text not null,
  relevance text not null,
  constraint paper_reviews_pkey primary key (id)
) TABLESPACE pg_default;

create index IF not exists idx_paper_metadata on public.paper_reviews using gin (metadata) TABLESPACE pg_default;

create index IF not exists idx_paper_methodology on public.paper_reviews using gin (methodology) TABLESPACE pg_default;
