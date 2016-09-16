drop table if exists users;
create table users (
user_name text NOT NULL PRIMARY KEY ,
category text NOT NULL );

drop table if exists user_details;
create table user_details (
user_name text NOT NULL PRIMARY KEY ,
ssh_pub_key text NOT NULL,
fingerprint text NOT NULL,
FOREIGN KEY(user_name) REFERENCES users(user_name) );

drop table if exists access_status;
create table access_status (
user_name text NOT NULL PRIMARY KEY,
status text NOT NULL,
env test NOT NULL,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
FOREIGN KEY(user_name) REFERENCES users(user_name) );

