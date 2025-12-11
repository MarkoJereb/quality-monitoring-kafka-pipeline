import psycopg2

class PostgresClient:
    def __init__(self, dsn):
        self.dsn = dsn
        self._conn = None

    def connect(self):
        if self._conn is None:
            self._conn = psycopg2.connect(self.dsn)
            self._conn.autocommit = True

    def insert_reading(self, ts, temperature, ph, moisture, alert):
        self.connect()
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sensor_readings (ts, temperature, ph, moisture, alert)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (ts, temperature, ph, moisture, alert)
            )
