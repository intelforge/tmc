-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS adversaries;
DROP TABLE IF EXISTS tactics;
DROP TABLE IF EXISTS techniques;
DROP TABLE IF EXISTS subtechniques;
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS adversaries_x_tools;
DROP TABLE IF EXISTS tools_x_techniques;
DROP TABLE IF EXISTS tactics_x_techniques;
DROP TABLE IF EXISTS techniques_x_subtechniques;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE adversaries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  adversary_name TEXT NOT NULL,
  adversary_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE tactics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tactic_name TEXT NOT NULL,
  tactic_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  technique_name TEXT NOT NULL,
  technique_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subtechnique_name TEXT NOT NULL,
  subtechnique_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_name TEXT NOT NULL,
  tool_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE adversaries_x_tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  adversary_id INTEGER NOT NULL,
  tool_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (adversary_id) REFERENCES adversary (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id)
);


CREATE TABLE tools_x_techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_id INTEGER NOT NULL,
  technique_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id)
);


CREATE TABLE tactics_x_techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tactic_id INTEGER NOT NULL,
  technique_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tactic_id) REFERENCES tactic (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id)
);

CREATE TABLE techniques_x_subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  technique_id INTEGER NOT NULL,
  subtechnique_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id),
  FOREIGN KEY (subtechnique_id) REFERENCES subtechnique (id)
);