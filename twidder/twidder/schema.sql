DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS messages;


CREATE TABLE user(email TEXT PRIMARY KEY NOT NULL,
  first_name TEXT NOT NULL,
  family_name TEXT NOT NULL,
  gender TEXT NOT NULL,
  city TEXT NOT NULL,
  country TEXT NOT NULL,
  password TEXT NOT NULL,
  token TEXT);

CREATE TABLE messages(
  receiving_user TEXT NOT NULL,
  sending_user TEXT NOT NULL,
  message TEXT NOT NULL
);

--CREATE TABLE signed_in_users (token TEXT PRIMARY KEY NOT NULL,
  --email TEXT NOT NULL);

INSERT INTO user (email, first_name, family_name, gender, city, country, password, token)
VALUES (        "qwe@q.q", "Q-Man",   "W-Name",  "Alien", "Titan","Mars", "qwe", "ASDASD" );

INSERT INTO messages(receiving_user, sending_user, message)
VALUES ("qwe@q.q", "thisisnotfake@q.q", "this is message");
INSERT INTO messages(receiving_user, sending_user, message)
VALUES ("qwe@q.q", "thisisnotfake@q.q", "another one!");

--INSERT INTO signed_in_users(email, token)
--VALUES ( "qwe@q.q", "ASDASD")
