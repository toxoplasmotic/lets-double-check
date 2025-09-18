import json
import csv
import sys
import os
import glob

# Check if a directory parameter is provided
if len(sys.argv) != 2:
    print("Usage: python json_to_csv.py <input_directory>")
    sys.exit(1)

# Get the input directory from command line argument
input_dir = sys.argv[1]

# Verify the directory exists
if not os.path.isdir(input_dir):
    print(f"Error: Directory '{input_dir}' does not exist.")
    sys.exit(1)

# Find all JSON files in the directory
json_files = glob.glob(os.path.join(input_dir, "*.json"))
if not json_files:
    print(f"Error: No JSON files found in directory '{input_dir}'.")
    sys.exit(1)

# Collect names from all JSON files
all_names = []
for json_file in json_files:
    try:
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            # Extract names from the JSON data
            names = [item["name"][0] for item in json_data["results"]]
            all_names.extend(names)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        continue
    except (json.JSONDecodeError, KeyError):
        print(f"Error: Invalid JSON format or missing 'results'/'name' in '{json_file}'.")
        continue

# Check if any names were collected
if not all_names:
    print("Error: No valid names extracted from JSON files.")
    sys.exit(1)

# Write to CSV in the input directory
output_file = os.path.join(input_dir, "counties.csv")
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for name in all_names:
        writer.writerow([name])