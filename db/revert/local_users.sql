-- Revert asyncrisk:local_users from pg

BEGIN;

--revoke permissions on the developer_account role

COMMIT;
