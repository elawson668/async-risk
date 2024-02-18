-- Revert transpo:user from pg

BEGIN;

DROP TABLE asyncrisk.requests;
DROP TABLE asyncrisk.friends;
DROP TABLE asyncrisk.users;

COMMIT;
