DROP TABLE IF EXISTS user;

CREATE TABLE user(email TEXT PRIMARY KEY NOT NULL,
  first_name TEXT NOT NULL,
  family_name TEXT NOT NULL,
  gender TEXT NOT NULL,
  city TEXT NOT NULL,
  country TEXT NOT NULL,
  password TEXT NOT NULL);

INSERT INTO user (email, first_name, family_name, gender, city, country, password)
VALUES (        "qwe@q.q", "Q-Man",   "W-Name",  "Alien", "Titan","Mars", "qwe" );
