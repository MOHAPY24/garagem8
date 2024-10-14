

# IMPORTS
import json
import os
from datetime import datetime


# Database Class
class M8DB:
    def __init__(self, db_file, log_file='log.txt'):
        """Initialize the database and log file paths."""
        self.db_file = db_file
        self.log_file = log_file
        # Create the database file if it doesn't exist
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)
        # Create the log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("=== Database Log ===\n")

    def _log(self, message):
        """Log a message with a timestamp to the log file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")

    def _read_db(self):
        """Read and return the entire database content."""
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def _write_db(self, data):
        """Write data to the JSON database."""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)

    def create(self, key, value):
        """Add a new entry to the database."""
        data = self._read_db()
        if key in data:
            self._log(f"Failed to create '{key}': Key already exists.")
            raise KeyError(f"Key '{key}' already exists.")
        data[key] = value
        self._write_db(data)
        self._log(f"Created new entry: '{key}'.")

    def read(self, key=None):
        """Read and return the entire database or a specific entry by key."""
        data = self._read_db()
        if key:
            entry = data.get(key, f"Key '{key}' not found.")
            self._log(f"Read entry: '{key}' -> {entry}")
            return entry
        self._log("Read entire database.")
        return data

    def update(self, key, value):
        """Update an existing entry in the database."""
        data = self._read_db()
        if key not in data:
            self._log(f"Failed to update '{key}': Key does not exist.")
            raise KeyError(f"Key '{key}' does not exist.")
        data[key] = value
        self._write_db(data)
        self._log(f"Updated entry: '{key}'.")

    def delete(self, key):
        """Delete an entry from the database."""
        data = self._read_db()
        if key not in data:
            self._log(f"Failed to delete '{key}': Key does not exist.")
            raise KeyError(f"Key '{key}' does not exist.")
        del data[key]
        self._write_db(data)
        self._log(f"Deleted entry: '{key}'.")

    def clear_db(self):
        """Clear all entries in the database."""
        self._write_db({})
        self._log("Cleared the entire database.")
