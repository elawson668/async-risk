-- Deploy asyncrisk:user to pg
-- requires: appschema

BEGIN;

-- USER

CREATE TABLE asyncrisk.users (
    id SERIAL primary key,
    username character varying(24) NOT NULL UNIQUE,
    email character varying(120) NOT NULL UNIQUE,
    password character varying(60) NOT NULL
);

-- FRIENDS

CREATE TABLE asyncrisk.friends (
    id SERIAL primary key,
    user_id integer NOT NULL,
    friend_id integer NOT NULL
);

ALTER TABLE ONLY asyncrisk.friends
ADD CONSTRAINT friends_user_id_fkey FOREIGN KEY (user_id) REFERENCES asyncrisk.users(id);

ALTER TABLE ONLY asyncrisk.friends
ADD CONSTRAINT friends_friend_id_fkey FOREIGN KEY (friend_id) REFERENCES asyncrisk.users(id);

-- REQUESTS

CREATE TABLE asyncrisk.requests (
    id SERIAL primary key,
    user_id integer NOT NULL,
    requester_id integer NOT NULL
);

ALTER TABLE ONLY asyncrisk.requests
ADD CONSTRAINT request_user_id_fkey FOREIGN KEY (user_id) REFERENCES asyncrisk.users(id);

ALTER TABLE ONLY asyncrisk.requests
ADD CONSTRAINT requests_requester_id_fkey FOREIGN KEY (requester_id) REFERENCES asyncrisk.users(id);

COMMIT;
