DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS content;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role INTEGER NOT NULL
);

CREATE TABLE contents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  access_level INTEGER NOT NULL,
  content TEXT NOT NULL
);
