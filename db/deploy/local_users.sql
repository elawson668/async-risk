-- Deploy asyncrisk:local_users to pg
-- requires: appschema

BEGIN;

GRANT ALL ON SCHEMA asyncrisk TO risk;
GRANT ALL ON ALL TABLES IN SCHEMA asyncrisk TO risk;
GRANT ALL ON ALL SEQUENCES IN SCHEMA asyncrisk TO risk;

COMMIT;
