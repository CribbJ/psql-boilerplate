-- 01-init.sql
-- Under user postgres (admin): psql -U postgres -d postgre -a -f 01-init.sql
-- 1. Create a new database
-- 2. Revoke all database and schema public from PUBLIC
-- 3. Create DDL role
-- 4. Create DML role

-- Create database for app
CREATE DATABASE name_of_database;

-- Revoke ALL on database and schema public from PUBLIC
REVOKE ALL ON DATABASE name_of_database FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- DDL role
CREATE ROLE ddl_role WITH ENCRYPTED PASSWORD 'password';
GRANT CONNECT ON DATABASE name_of_database TO ddl_role;
GRANT TEMPORARY ON DATABASE name_of_database TO ddl_role;

-- DML role
CREATE ROLE dml_role WITH ENCRYPTED PASSWORD 'password';
GRANT CONNECT ON name_of_database TO dml_role;
GRANT TEMPORARY ON DATABASE name_of_database TO dml_role;