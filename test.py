# Imports

import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class JsonDatabase:
    def __init__(self, db_file='test/dbtest.json', log_file='test/logtest.txt'):
        """Initialize the database and log file paths."""
        self.db_file = db_file
        self.log_file = log_file
        # Create the database file if it doesn't exist
        if not os.path.exists(self.db_file):
            with open("test/"+self.db_file, 'w') as f:
                json.dump({}, f)
        # Create the log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open("test/"+self.log_file, 'w') as f:
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

class DatabaseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = JsonDatabase('test/dbtest.json')

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input for key
        self.key_input = TextInput(hint_text='Enter Key', multiline=False)
        self.layout.add_widget(self.key_input)

        # Input for value
        self.value_input = TextInput(hint_text='Enter Value (JSON format)', multiline=False)
        self.layout.add_widget(self.value_input)

        # Buttons for CRUD operations
        button_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)

        button_layout.add_widget(Button(text='Create', on_press=self.create_entry))
        button_layout.add_widget(Button(text='Read', on_press=self.read_entry))
        button_layout.add_widget(Button(text='Update', on_press=self.update_entry))
        button_layout.add_widget(Button(text='Delete', on_press=self.delete_entry))
        button_layout.add_widget(Button(text='Clear', on_press=self.clear_db))

        self.layout.add_widget(button_layout)

        # Output area
        self.output_area = ScrollView()
        self.output_label = Label(size_hint_y=None)
        self.output_label.bind(size=self.output_label.setter('text_size'))
        self.output_area.add_widget(self.output_label)
        self.layout.add_widget(self.output_area)

        return self.layout

    def create_entry(self, instance):
        key = self.key_input.text
        value = self.value_input.text
        try:
            self.db.create(key, json.loads(value))
            self.output_label.text = f"Entry '{key}' created."
        except Exception as e:
            self.output_label.text = str(e)

    def read_entry(self, instance):
        key = self.key_input.text
        if key:
            value = self.db.read(key)
            self.output_label.text = f"Value for '{key}': {value}"
        else:
            self.output_label.text = f"All entries: {self.db.read()}"

    def update_entry(self, instance):
        key = self.key_input.text
        value = self.value_input.text
        try:
            self.db.update(key, json.loads(value))
            self.output_label.text = f"Entry '{key}' updated."
        except Exception as e:
            self.output_label.text = str(e)

    def delete_entry(self, instance):
        key = self.key_input.text
        try:
            self.db.delete(key)
            self.output_label.text = f"Entry '{key}' deleted."
        except Exception as e:
            self.output_label.text = str(e)

    def clear_db(self, instance):
        self.db.clear_db()
        self.output_label.text = "Database cleared."

if __name__ == '__main__':
    DatabaseApp().run()