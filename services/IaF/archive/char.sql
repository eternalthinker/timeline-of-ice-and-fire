CREATE TABLE characters(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  slug TEXT,
  gender TEXT,
  culture TEXT,
  titles TEXT,
  aliases TEXT,
  father TEXT,
  mother TEXT,
  spouse TEXT,
  allegiances TEXT,
  seasons TEXT,
  actor TEXT

);

CREATE TABLE houses(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  slug TEXT,
  region TEXT,
  coatOfArms TEXT,
  words TEXT,
  titles TEXT,
  seats TEXT,
  currentLord TEXT,
  overlord TEXT,
  swornMembers TEXT

);

