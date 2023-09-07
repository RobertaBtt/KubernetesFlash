CREATE TABLE IF NOT EXISTS CSV (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                url CHAR NOT NULL UNIQUE,
                                topic CHAR NOT NULL);
