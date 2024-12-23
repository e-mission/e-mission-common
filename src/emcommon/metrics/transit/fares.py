import json
import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pyperclip
import webbrowser

# File path for saving the fare data
output_file = 'fare_link.json'

# Function to load existing fare data if the JSON file exists and is valid
def load_existing_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                else:
                    return {}  # If data is not a valid dictionary, return empty dict
        except (json.JSONDecodeError, ValueError):
            return {}  # If there's a decoding error, return an empty dict
    return {}

# Function to save fare data to a JSON file
def save_fare_data(file_path, fare_data):
    with open(file_path, 'w') as f:
        json.dump(fare_data, f, indent=4)

# Function to handle clipboard data capture
def capture_clipboard(dba, current_index, total, root):
    clipboard_content = pyperclip.paste().strip()
    fare_data = load_existing_data(output_file)
    fare_data[dba] = {"fare_link": clipboard_content}
    save_fare_data(output_file, fare_data)
    print(f"Saved link for {dba}: {clipboard_content}")

    # Proceed to next DBA or finish if done
    if current_index < total - 1:
        root.destroy()  # Close the current window to move to the next
        next_dba(current_index + 1, total, df)
    else:
        messagebox.showinfo("Done", "All DBAs processed!")
        root.destroy()

# Function to trigger web search and clipboard capture
def search_fare(dba, current_index, total, root):
    webbrowser.open(f"https://www.google.com/search?q={dba}+bus+fare")
    messagebox.showinfo("Next Step", f"Search results for {dba} opened. Copy the link, then press 'OK' to save it.")
    
    # After clicking OK, capture clipboard content
    capture_clipboard(dba, current_index, total, root)

# Function to iterate DBAs and process each one
def next_dba(current_index, total, df):
    dba = df.iloc[current_index]['Agency']  # Get 'Agency' from DataFrame
    # Create a new tkinter window for each DBA
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    search_fare(dba, current_index, total, root)

# Main function to initiate processing, skipping agencies already in JSON
def process_dbas(df):
    fare_data = load_existing_data(output_file)
    df = df[~df['Agency'].isin(fare_data.keys())]  # Remove agencies already in JSON
    total_rows = len(df)
    if total_rows == 0:
        messagebox.showinfo("Done", "All agencies have been processed!")
    else:
        next_dba(0, total_rows, df)

# Load the DataFrame from the pickle file
df = pd.read_pickle('ntd.pkl')
df = df.drop_duplicates(subset='Agency')

# Start processing the DBAs
process_dbas(df)
