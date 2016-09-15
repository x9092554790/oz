CREATE DATABASE server_db;
CREATE user server_db_user with password 'sdg5g4123';
ALTER ROLE server_db_user SET client_encoding TO 'utf8';
ALTER ROLE server_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE server_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE server_db TO server_db_user;
