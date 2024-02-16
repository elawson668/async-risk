-- Verify transpo:user on pg

BEGIN;

-- USER

SELECT
  id,
  username,
  email,
  password
FROM asyncrisk.users
WHERE FALSE;

SELECT *
FROM asyncrisk.user_id_seq
WHERE FALSE;

ROLLBACK;
