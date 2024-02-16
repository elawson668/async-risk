-- Verify async-risk:appschema on pg

BEGIN;

-- XXX Add verifications here.

SELECT pg_catalog.has_schema_privilege('asyncrisk', 'usage');

ROLLBACK;
