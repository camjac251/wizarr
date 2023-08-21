from app.models.database.base import db
from cryptography.fernet import Fernet, InvalidToken
from base64 import urlsafe_b64encode
from flask import request, make_response
from datetime import datetime
from json import dumps, loads

def backup_database():

    # Backup dictionary
    backup = {}

    # Get all tables
    db_tables = db.get_tables()

    # Get all rows in the table
    for table in db_tables:

        # Add the table to the backup dictionary
        backup[table] = []

        # Get all rows in the table
        db_rows = db.execute_sql(f"SELECT * FROM {table}")

        # Get all columns in the table
        db_columns = [column[0] for column in db_rows.description]

        # Add all rows to the backup dictionary
        for row in db_rows:
            backup[table].append(dict(zip(db_columns, row)))

    # Remove apscheduler_jobs table
    backup.pop("apscheduler_jobs", None)

    return backup


def generate_key(text):
    # Convert the text to bytes
    text = text.encode()

    # Pad the text to 32 bytes
    text = text + b"=" * (32 - len(text) % 32)

    # Encode the text to base64
    text = urlsafe_b64encode(text).decode()

    # Return the base64 encoded text
    return text


def encrypt_backup(backup: dict, key: str):
    # Create the encryption key
    key = Fernet(key)

    def encrypt_string(string: str):
        return key.encrypt(string.encode()).decode()

    backup_string = dumps(backup)
    encrypted_backup = encrypt_string(backup_string)

    return encrypted_backup


def decrypt_backup(backup: str, key: str):
    # Create the encryption key
    key = Fernet(key)

    def decrypt_string(string: str):
        return key.decrypt(string).decode()

    backup_string = decrypt_string(backup)

    return loads(backup_string)
