-- 02-init.sql
-- 1. Revoke create on schema public from PUBLIC
-- 2. Schema creation
-- 3. Create user login roles
-- 4. GRANT ddl usage to CREATE
-- 5. GRANT dml usage to SELECT
-- 6. Assign to specific roles

-- Revoke create on schema public from PUBLIC
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Create new schema
CREATE SCHEMA IF NOT EXISTS myschema;

-- Create 2 roles. CHANGE THIS IF NEEDED
-- 1. Flyway user (ddl_role)
-- 2. App user (dml_role)
CREATE USER flywayuser WITH ENCRYPTED PASSWORD 'password';
CREATE USER appuser WITH ENCRYPTED PASSWORD 'password';

-- ddl_role has CREATE on schema
GRANT USAGE CREATE ON SCHEMA myschema TO ddl_role;
GRANT ALL ON ALL SEQUENCES myschema TO ddl_role;

-- dml_role has SELECT on schema
GRANT USAGE ON SCHEMA myschema TO dml_role;
GRANT USAGE SELECT ON ALL SEQUENCES myschema TO dml_role;

-- Assign users to specific roles
GRANT ddl_role TO flywayuser;
GRANT dml_role TO appuser;
