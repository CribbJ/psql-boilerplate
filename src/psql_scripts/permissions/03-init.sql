-- 03-init.sql
-- Alter specific privileges for the schema (future)

ALTER DEFAULT PRIVILEGES IN SCHEMA myschema
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dml_role;