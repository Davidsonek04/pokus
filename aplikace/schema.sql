DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS insurance;
DROP TABLE IF EXISTS administration;

CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT UNIQUE NOT NULL,
name TEXT NOT NULL,
surname TEXT NOT NULL,
tel INTEGER NOT NULL,
street_descriptive TEXT NOT NULL,
city TEXT NOT NULL,
zip_code INTEGER NOT NULL
);

CREATE TABLE insurance (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
insurance INTEGER NOT NULL,
amound INTEGER NOT NULL,
subject TEXT NOT NULL,
valid_from TEXT NOT NULL,
valid_until TEXT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE administration (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
surname TEXT NOT NULL,
password TEXT NOT NULL,
email TEXT UNIQUE NOT NULL
);

--  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--  body TEXT NOT NULL,