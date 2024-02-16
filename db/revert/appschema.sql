-- Revert async-risk:appschema from pg

BEGIN;

DROP SCHEMA asyncrisk;

COMMIT;
