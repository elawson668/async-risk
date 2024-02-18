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

-- FRIENDS

SELECT
  id,
  user_id,
  friend_id
FROM asyncrisk.friends
WHERE FALSE;

-- REQUESTS

SELECT
  id,
  user_id,
  requester_id
FROM asyncrisk.requests
WHERE FALSE;

ROLLBACK;
