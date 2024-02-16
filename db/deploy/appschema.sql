-- Deploy asyncrisk:appschema to pg

BEGIN;

CREATE SCHEMA asyncrisk;
ALTER DATABASE risk SET search_path=asyncrisk;

COMMIT;
