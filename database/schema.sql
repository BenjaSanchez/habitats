CREATE TABLE IF NOT EXISTS sensors (
    device_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    collected_at INTEGER NOT NULL,
    temperature REAL,
    temperature_timestamp INTEGER,
    humidity REAL,
    humidity_timestamp INTEGER,
    FOREIGN KEY (device_id) REFERENCES sensors(device_id),
    UNIQUE (device_id, collected_at)
);

CREATE INDEX IF NOT EXISTS idx_readings_device_time
ON readings (device_id, collected_at);

CREATE INDEX IF NOT EXISTS idx_readings_time
ON readings (collected_at);
