-- USER TABLE
CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  -- TODO: do we need to store passwords here?
  -- TODO:the fields below are all things that we may find relevant to consider
  -- gender CHAR(1) NOT NULL, -- M, F, O
  -- age INT NOT NULL,
  -- country TEXT NOT NULL,
  -- lang TEXT NOT NULL,
  UNIQUE(username)
);

-- USER search log table
-- this includes search method (so, query type, ranking type, etc)
-- as well as the time of the search and the query itself
CREATE TABLE log_search (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  search_time INTEGER NOT NULL,
  query TEXT NOT NULL,
  query_type TEXT NOT NULL,
  ranking_type TEXT DEFAULT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

-- USER retrieved page log table
CREATE TABLE log_retrieved (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  search_time INTEGER NOT NULL,
  doc_id TEXT NOT NULL,
  idx TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

-- USER profile vector
CREATE TABLE usr_profile_vector (
  user_id INTEGER NOT NULL,
  search_time INTEGER NOT NULL,
  score FLOAT NOT NULL,
  -- TODO: this may/should require more fields, can be discussed later
  PRIMARY KEY (user_id),
  FOREIGN KEY(user_id) REFERENCES users(id)
);