# Import necessary libraries
import sqlite3  # SQLite3 library for handling database operations
import json  # JSON library for serialization and deserialization of data
from utils.UserProfile import UserProfile  # Importing the UserProfile class that defines the structure of user profile objects
import os

# Function to create a SQLite database and initialize the user_profiles table
def create_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('user_profiles.db')
    cursor = connection.cursor()
    
    # SQL query to create a user_profiles table if it does not already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            search_history TEXT,
            click_history TEXT,
            category_preferences TEXT,
            term_preferences TEXT
        )
    ''')
    
    # Commit changes to the database and close the connection
    connection.commit()
    connection.close()
    print("Database and table created successfully.")

# Function to delete the SQLite database file
def delete_db():
    # Try to remove the database file
    try:
        os.remove("user_profiles.db")
        print("Database deleted successfully.")
    except FileNotFoundError:
        # Handle the case where the database file is not found
        print("Database file not found.")

# Function to save or update a user profile in the database
def save_user_profile(user_profile):
    # Connect to the database
    connection = sqlite3.connect('user_profiles.db')
    cursor = connection.cursor()
    
    # SQL query to insert or update a user profile
    cursor.execute('''
        INSERT INTO user_profiles (user_id, search_history, click_history, category_preferences, term_preferences) VALUES
        (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
        search_history=excluded.search_history,
        click_history=excluded.click_history,
        category_preferences=excluded.category_preferences,
        term_preferences=excluded.term_preferences;
    ''', (
        user_profile.user_id,
        json.dumps(user_profile.search_history),
        json.dumps(user_profile.click_history),
        json.dumps(user_profile.category_preferences),
        json.dumps(user_profile.term_preferences)
    ))
    
    # Commit changes and close the database connection
    connection.commit()
    connection.close()

# Function to load a user profile from the database
def load_user_profile(user_id):
    # Connect to the database
    connection = sqlite3.connect('user_profiles.db')
    cursor = connection.cursor()
    
    # Query the database for a user profile by user_id
    cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    connection.close()
    
    # Check if a row was returned
    if row:
        # Deserialize JSON data into Python objects and return a populated UserProfile instance
        user_profile = UserProfile(row[0])
        user_profile.search_history = json.loads(row[1])
        user_profile.click_history = json.loads(row[2])
        user_profile.category_preferences = json.loads(row[3])
        user_profile.term_preferences = json.loads(row[4])
        return user_profile
    else:
        # Return a new UserProfile instance if no profile was found
        return UserProfile(user_id)

# Main section to run the script interactively
if __name__ == "__main__":
    print("1. Create Database")
    print("2. Delete Database and recreate a new one")
    choice = input("Choose an option (1 or 2): ")
    
    # Handle user input
    if choice == '1':
        create_db()
    elif choice == '2':
        delete_db()
        create_db()
    else:
        print("Invalid choice. Exiting.")
