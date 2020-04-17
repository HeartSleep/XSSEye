-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.3-alpha
-- PostgreSQL version: 12.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- object: xsseye_user | type: ROLE --
-- DROP ROLE IF EXISTS xsseye_user;
CREATE ROLE xsseye_user WITH 
	LOGIN
	ENCRYPTED PASSWORD 'e7wnrh30hbs';
-- ddl-end --


-- Database creation must be done outside a multicommand file.
-- These commands were put in this file only as a convenience.
-- -- object: xsseye | type: DATABASE --
-- -- DROP DATABASE IF EXISTS xsseye;
-- CREATE DATABASE xsseye;
-- -- ddl-end --
-- 

-- object: users | type: SCHEMA --
-- DROP SCHEMA IF EXISTS users CASCADE;
CREATE SCHEMA users;
-- ddl-end --
ALTER SCHEMA users OWNER TO xsseye_user;
-- ddl-end --

-- object: reports | type: SCHEMA --
-- DROP SCHEMA IF EXISTS reports CASCADE;
CREATE SCHEMA reports;
-- ddl-end --
ALTER SCHEMA reports OWNER TO xsseye_user;
-- ddl-end --

-- object: xsseye | type: SCHEMA --
-- DROP SCHEMA IF EXISTS xsseye CASCADE;
CREATE SCHEMA xsseye;
-- ddl-end --
ALTER SCHEMA xsseye OWNER TO xsseye_user;
-- ddl-end --

-- object: notifications_settings | type: SCHEMA --
-- DROP SCHEMA IF EXISTS notifications_settings CASCADE;
CREATE SCHEMA notifications_settings;
-- ddl-end --
ALTER SCHEMA notifications_settings OWNER TO xsseye_user;
-- ddl-end --

SET search_path TO pg_catalog,public,users,reports,xsseye,notifications_settings;
-- ddl-end --

-- object: users."user" | type: TABLE --
-- DROP TABLE IF EXISTS users."user" CASCADE;
CREATE TABLE users."user" (
	id serial NOT NULL,
	username text,
	password text,
	email text,
	telegram_id integer,
	all_domains bool DEFAULT FALSE,
	is_admin bool DEFAULT FALSE,
	CONSTRAINT users_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE users."user" OWNER TO xsseye_user;
-- ddl-end --

INSERT INTO users."user" (id, password, email, telegram_id, all_domains, is_admin, username) VALUES (E'1', E'pbkdf2:sha256:150000$Sop807IB$8ff198d5bf01d040fe743327f5263f00659400be3799640871563d7b9880455a', E'nstikhomirov@gmail.com', E'106936600', E'TRUE', E'TRUE', E'NSTikhomirov');
-- ddl-end --

-- object: users.domains_access | type: TABLE --
-- DROP TABLE IF EXISTS users.domains_access CASCADE;
CREATE TABLE users.domains_access (
	id serial NOT NULL,
	domain text,
	id_user integer,
	CONSTRAINT domains_access_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE users.domains_access OWNER TO xsseye_user;
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE users.domains_access DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE users.domains_access ADD CONSTRAINT user_fk FOREIGN KEY (id_user)
REFERENCES users."user" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: domains_access_users_uniq | type: CONSTRAINT --
-- ALTER TABLE users.domains_access DROP CONSTRAINT IF EXISTS domains_access_users_uniq CASCADE;
ALTER TABLE users.domains_access ADD CONSTRAINT domains_access_users_uniq UNIQUE (domain,id_user);
-- ddl-end --

-- object: xsseye.reports | type: TABLE --
-- DROP TABLE IF EXISTS xsseye.reports CASCADE;
CREATE TABLE xsseye.reports (
	id serial NOT NULL,
	id_payload integer,
	uniq_id uuid,
	is_https bool DEFAULT FALSE,
	hostname text,
	port integer DEFAULT 80,
	path text DEFAULT '/',
	query text,
	hash text,
	client_ip inet,
	user_agent text,
	cookies json DEFAULT '{}'::json,
	localstorage json DEFAULT '{}'::json,
	additional_data json DEFAULT '{}'::json,
	referrer text,
	CONSTRAINT reports_id_pk PRIMARY KEY (id),
	CONSTRAINT reports_uniq_id_uniq UNIQUE (uniq_id)

);
-- ddl-end --
ALTER TABLE xsseye.reports OWNER TO xsseye_user;
-- ddl-end --

-- object: xsseye.payloads | type: TABLE --
-- DROP TABLE IF EXISTS xsseye.payloads CASCADE;
CREATE TABLE xsseye.payloads (
	id serial NOT NULL,
	uniq_id uuid,
	public_id text NOT NULL,
	id_owner integer,
	CONSTRAINT payloads_id_pk PRIMARY KEY (id),
	CONSTRAINT payloads_uniq_id_uniq UNIQUE (uniq_id)

);
-- ddl-end --
ALTER TABLE xsseye.payloads OWNER TO postgres;
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE xsseye.payloads DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE xsseye.payloads ADD CONSTRAINT user_fk FOREIGN KEY (id_owner)
REFERENCES users."user" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: payloads_fk | type: CONSTRAINT --
-- ALTER TABLE xsseye.reports DROP CONSTRAINT IF EXISTS payloads_fk CASCADE;
ALTER TABLE xsseye.reports ADD CONSTRAINT payloads_fk FOREIGN KEY (id_payload)
REFERENCES xsseye.payloads (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: notifications_settings.telegram_bot | type: TABLE --
-- DROP TABLE IF EXISTS notifications_settings.telegram_bot CASCADE;
CREATE TABLE notifications_settings.telegram_bot (
	id serial NOT NULL,
	access_token text NOT NULL,
	name text,
	CONSTRAINT telegram_bot_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE notifications_settings.telegram_bot OWNER TO postgres;
-- ddl-end --

-- object: notifications_settings.telegram_bot_logs | type: TABLE --
-- DROP TABLE IF EXISTS notifications_settings.telegram_bot_logs CASCADE;
CREATE TABLE notifications_settings.telegram_bot_logs (
	id bigserial NOT NULL,
	sended_text text,
	id_bot integer,
	id_user integer NOT NULL,
	CONSTRAINT telegram_bot_logs_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE notifications_settings.telegram_bot_logs OWNER TO postgres;
-- ddl-end --

-- object: telegram_bot_fk | type: CONSTRAINT --
-- ALTER TABLE notifications_settings.telegram_bot_logs DROP CONSTRAINT IF EXISTS telegram_bot_fk CASCADE;
ALTER TABLE notifications_settings.telegram_bot_logs ADD CONSTRAINT telegram_bot_fk FOREIGN KEY (id_bot)
REFERENCES notifications_settings.telegram_bot (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE notifications_settings.telegram_bot_logs DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE notifications_settings.telegram_bot_logs ADD CONSTRAINT user_fk FOREIGN KEY (id_user)
REFERENCES users."user" (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: users_username_uniq | type: INDEX --
-- DROP INDEX IF EXISTS users.users_username_uniq CASCADE;
CREATE UNIQUE INDEX users_username_uniq ON users."user"
	USING btree
	(
	  (lower(username))
	);
-- ddl-end --


