CREATE TABLE IF NOT EXISTS sensor_readings (
    id serial PRIMARY KEY,
    ts timestamptz NOT NULL,
    temperature numeric NOT NULL,
    ph numeric NOT NULL,
    moisture numeric NOT NULL,
    alert boolean NOT NULL DEFAULT false
);
