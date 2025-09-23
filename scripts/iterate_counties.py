import os
import subprocess

def iterate_counties():
    """Iterate through states/{stateName}/{shortCountyName} directories and call create_county_info.py."""
    states_dir = "states"
    if not os.path.exists(states_dir):
        print(f"Error: Directory '{states_dir}' does not exist.")
        return

    for state_name in os.listdir(states_dir):
        state_path = os.path.join(states_dir, state_name)
        if not os.path.isdir(state_path):
            continue  # Skip non-directory files
        for county_name in os.listdir(state_path):
            county_path = os.path.join(state_path, county_name)
            if not os.path.isdir(county_path):
                continue  # Skip non-directory files
            output_file = os.path.join(county_path, "county_info.xml")
            # Run create_county_info.py with state, county, and output file
            cmd = ["python3", "scripts/create_county_info.py", state_name, county_name, output_file]
            print(f"Running: {' '.join(cmd)}")
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error processing {state_name}, {county_name}: {e}")
                print(e.stderr)

if __name__ == "__main__":
    iterate_counties()