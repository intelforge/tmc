-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS adversaries;
DROP TABLE IF EXISTS tactics;
DROP TABLE IF EXISTS techniques;
DROP TABLE IF EXISTS subtechniques;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS industries;
DROP TABLE IF EXISTS event_x_industry;
DROP TABLE IF EXISTS adversaries_x_tools;
DROP TABLE IF EXISTS tools_x_techniques;
DROP TABLE IF EXISTS tools_x_subtechniques;
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
  adversary_id TEXT NOT NULL,
  adversary_name TEXT NOT NULL,
  adversary_description TEXT NOT NULL,
  adversary_identifiers TEXT,
  adversay_sorigin TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE tactics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tactic_id TEXT NOT NULL,
  tactic_name TEXT NOT NULL,
  tactic_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  technique_id TEXT NOT NULL,
  technique_name TEXT NOT NULL,
  technique_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subtechnique_id TEXT NOT NULL,
  subtechnique_name TEXT NOT NULL,
  subtechnique_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_id TEXT NOT NULL,
  tool_name TEXT NOT NULL,
  tool_description TEXT NOT NULL,
  tool_identifiers TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_id TEXT NOT NULL,
  event_name TEXT NOT NULL,
  event_description TEXT NOT NULL,
  event_industry TEXT,
  event_date DATETIME,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE adversaries_x_tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  adversary_id TEXT NOT NULL,
  tool_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (adversary_id) REFERENCES adversary (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id)
);


CREATE TABLE tools_x_techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_id TEXT NOT NULL,
  technique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id)
);

CREATE TABLE tools_x_subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_id TEXT NOT NULL,
  subtechnique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id),
  FOREIGN KEY (subtechnique_id) REFERENCES subtechnique (id)
);

CREATE TABLE tactics_x_techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tactic_id TEXT NOT NULL,
  technique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tactic_id) REFERENCES tactic (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id)
);

CREATE TABLE techniques_x_subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  technique_id TEXT NOT NULL,
  subtechnique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id),
  FOREIGN KEY (subtechnique_id) REFERENCES subtechnique (id)
);


-- Industries taken from STIX
-- https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_oogrswk3onck

CREATE TABLE industries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  industry_name TEXT NOT NULL,
  industry_description TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE event_x_industry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_id TEXT NOT NULL,
  industry_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (event_id) REFERENCES event (id),
  FOREIGN KEY (industry_id) REFERENCES industry (id)
);


INSERT INTO industries (author_id, industry_name) 
VALUES (1, 'Agriculture'),
(1, 'Aerospace'),
(1, 'Automotive'),
(1, 'Chemical'),
(1, 'Commercial'),
(1, 'Communications'),
(1, 'Construction'),
(1, 'Defense'),
(1, 'Education'),
(1, 'Energy'),
(1, 'Entertainment'),
(1, 'Financial Services'),
(1, 'Government'),
(1, 'Healthcare'),
(1, 'Hospitality & Leisure'),
(1, 'Infrastructure'),
(1, 'Insurance'),
(1, 'Manufacturing'),
(1, 'Mining'),
(1, 'Non-profit'),
(1, 'Pharmaceuticals'),
(1, 'Retail'),
(1, 'Technology'),
(1, 'Telecommunications'),
(1, 'Transportation'),
(1, 'Utilities'),
(1, 'Unspecified');