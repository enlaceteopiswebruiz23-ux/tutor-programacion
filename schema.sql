-- Ejecutar UNA vez en Supabase: SQL Editor -> New query -> Run
create extension if not exists vector;

-- Etapa 1 y 3: historial de la conversación
create table if not exists mensajes (
  id bigint generated always as identity primary key,
  sesion text not null,
  rol text not null,
  contenido text not null,
  creado timestamptz default now()
);
create index if not exists mensajes_sesion_idx on mensajes (sesion, id);

-- Etapa 4: apuntes con su embedding (1536 dimensiones = text-embedding-3-small)
create table if not exists apuntes (
  id bigint generated always as identity primary key,
  archivo text,
  contenido text not null,
  embedding vector(1536)
);

-- Búsqueda por significado
create or replace function buscar_apuntes(query_embedding vector(1536), cantidad int default 3)
returns table (id bigint, archivo text, contenido text, similitud float)
language sql stable as $$
  select a.id, a.archivo, a.contenido,
         1 - (a.embedding <=> query_embedding) as similitud
  from apuntes a
  order by a.embedding <=> query_embedding
  limit cantidad;
$$;
