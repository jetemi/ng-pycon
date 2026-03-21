#!/usr/bin/env bash
# Runs once on first database init (empty volume). Creates the schema Django uses via search_path
# and sets it as the default for the user so it works through pgbouncer (which drops per-connection options).
set -euo pipefail
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE SCHEMA IF NOT EXISTS pyconng AUTHORIZATION "${POSTGRES_USER}";
	ALTER ROLE "${POSTGRES_USER}" SET search_path TO pyconng, public;
EOSQL
