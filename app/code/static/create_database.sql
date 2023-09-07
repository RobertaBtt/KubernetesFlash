CREATE TABLE IF NOT EXISTS CSV (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                url CHAR NOT NULL UNIQUE,
                                topic CHAR NOT NULL);

CREATE TABLE IF NOT EXISTS TOPIC (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name CHAR NOT NULL UNIQUE);