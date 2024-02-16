-- Revert transpo:user from pg

BEGIN;

DROP TABLE asyncrisk.users;

COMMIT;
