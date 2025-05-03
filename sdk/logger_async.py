"""
Asynchronous Logger for DriftBench SDK

Queues log messages and writes them to an SQLite database in a background thread.
Handles automatic schema creation.
"""

import sqlite3
import queue
import threading
import time
import os
import json

# Configuration
DB_NAME = "driftbench_log.db"
DB_PATH = os.path.join(os.path.dirname(__file__), "..", DB_NAME) # Place DB in root
QUEUE_MAX_SIZE = 1000 # Max items before potentially blocking/falling back
FLUSH_INTERVAL = 5 # Seconds
FLUSH_BATCH_SIZE = 100 # Max records per commit

# Database Schema (from blueprint)
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS corrections_log (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  file       TEXT,
  line       INT,
  issue      TEXT,
  correction TEXT,
  ts         TEXT DEFAULT CURRENT_TIMESTAMP,
  std_ver    TEXT,
  raw_json   TEXT,
  fixed_json TEXT,
  quality    REAL,
  pod_id     TEXT,
  req_id     TEXT
);
"""

INSERT_LOG_SQL = """
INSERT INTO corrections_log (
    file, line, issue, correction, std_ver, raw_json, fixed_json, quality, pod_id, req_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

class AsyncLogger:
    def __init__(self, db_path=DB_PATH, queue_max_size=QUEUE_MAX_SIZE):
        self.db_path = db_path
        self.log_queue = queue.Queue(maxsize=queue_max_size)
        self._stop_event = threading.Event()
        self._writer_thread = threading.Thread(target=self._db_writer, daemon=True)
        self._ensure_db_schema()
        self._writer_thread.start()
        print(f"AsyncLogger initialized. Writing to: {self.db_path}")

    def _ensure_db_schema(self):
        """Creates the database and table if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(CREATE_TABLE_SQL)
                # Optionally create the view as well
                # cursor.execute("DROP VIEW IF EXISTS quality_bucket;")
                # cursor.execute(CREATE_VIEW_SQL) # Define CREATE_VIEW_SQL from blueprint if needed
                conn.commit()
            print("Database schema verified/created.")
        except sqlite3.Error as e:
            print(f"Error ensuring database schema: {e}")
            # Handle error appropriately, maybe fallback or raise

    def _db_writer(self):
        """Background thread function to write logs from the queue to the DB."""
        print("DB writer thread started.")
        while not self._stop_event.is_set() or not self.log_queue.empty():
            logs_to_write = []
            try:
                # Collect logs in batches or wait for FLUSH_INTERVAL
                log_item = self.log_queue.get(timeout=FLUSH_INTERVAL)
                logs_to_write.append(log_item)
                # Drain queue up to BATCH_SIZE
                while len(logs_to_write) < FLUSH_BATCH_SIZE:
                    try:
                        log_item = self.log_queue.get_nowait()
                        logs_to_write.append(log_item)
                    except queue.Empty:
                        break # No more items for now

            except queue.Empty:
                # Timed out waiting for logs, loop continues
                continue
            except Exception as e:
                print(f"Error getting log from queue: {e}")
                time.sleep(1) # Avoid busy-looping on error
                continue

            if logs_to_write:
                try:
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        # Convert dicts to tuples for executemany
                        log_tuples = [
                            (
                                log.get("file"), log.get("line"), log.get("issue"),
                                log.get("correction"), log.get("std_ver"),
                                json.dumps(log.get("raw_json")) if log.get("raw_json") else None,
                                json.dumps(log.get("fixed_json")) if log.get("fixed_json") else None,
                                log.get("quality"), log.get("pod_id"), log.get("req_id")
                            ) for log in logs_to_write
                        ]
                        cursor.executemany(INSERT_LOG_SQL, log_tuples)
                        conn.commit()
                        for _ in logs_to_write:
                             self.log_queue.task_done()
                        # print(f"Flushed {len(logs_to_write)} logs to DB.") # Debug
                except sqlite3.Error as e:
                    print(f"Error writing logs to database: {e}")
                    # TODO: Implement retry or error handling (e.g., put logs back?)
                except Exception as e:
                    print(f"Unexpected error during DB write: {e}")

        print("DB writer thread stopped.")

    def log(self, log_entry: dict):
        """Enqueue a log entry (dictionary)."""
        try:
            # Blueprint mentions fallback to sync if queue full - for now, just block or drop
            # For a simple stub, we might just block with timeout or drop
            self.log_queue.put(log_entry, block=True, timeout=1) # Block for 1s
        except queue.Full:
            print("Warning: Log queue is full. Log entry dropped.")
            # Or implement synchronous write as fallback here
        except Exception as e:
            print(f"Error adding log to queue: {e}")

    def shutdown(self):
        """Signal the writer thread to stop and wait for it to finish."""
        print("Shutting down logger...")
        self._stop_event.set()
        self.log_queue.join() # Wait for queue to be empty
        self._writer_thread.join() # Wait for thread to exit
        print("Logger shut down complete.")

# Global logger instance (optional, depends on usage pattern)
# logger = AsyncLogger()

# Example Usage (for testing):
if __name__ == "__main__":
    logger = AsyncLogger()
    print("Sending test logs...")
    for i in range(5):
        logger.log({
            "file": f"test_file_{i}.py",
            "line": 10 + i,
            "issue": "Test Issue",
            "correction": "Test Correction",
            "std_ver": "1.0.0",
            "raw_json": {"original": f"code {i}"},
            "fixed_json": {"fixed": f"code {i} fixed"},
            "quality": 0.95 - (i * 0.02),
            "pod_id": f"pod-xyz-{i}",
            "req_id": f"req-abc-{i}"
        })
        time.sleep(0.1)

    print("Waiting for logs to flush...")
    logger.shutdown()

    # Verify DB content (manual check or add query code)
    print(f"Check the database file: {DB_PATH}")

