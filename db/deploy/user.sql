-- Deploy asyncrisk:user to pg
-- requires: appschema

BEGIN;

-- USER

CREATE TABLE asyncrisk.users (
    id integer NOT NULL,
    username character varying(24) NOT NULL,
    email character varying(120) NOT NULL,
    password character varying(60) NOT NULL
);


CREATE SEQUENCE asyncrisk.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE asyncrisk.user_id_seq OWNED BY asyncrisk.users.id;
ALTER TABLE ONLY asyncrisk.users ALTER COLUMN id SET DEFAULT nextval('asyncrisk.user_id_seq'::regclass);

ALTER TABLE ONLY asyncrisk.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY asyncrisk.users
    ADD CONSTRAINT user_email_key UNIQUE (email);

ALTER TABLE ONLY asyncrisk.users
    ADD CONSTRAINT user_username_key UNIQUE (username);

COMMIT;
