
import os

with open("us_states.txt", "r") as f:
    states = f.readlines()

for state in states:
    state = state.strip()
    if state:
        os.makedirs(os.path.join("states", state), exist_ok=True)


