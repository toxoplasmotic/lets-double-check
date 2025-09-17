
states = ["Virginia", "Nebraska", "Delaware", "Utah", "Alaska", "Arizona", "Hawaii", "Arkansas", "Illinois", "New York", "Kansas", "Montana", "Missouri", "Pennsylvania", "Wyoming", "Tennessee", "Ohio", "Vermont", "Idaho", "North Dakota", "Louisiana", "Oklahoma", "Texas", "Mississippi", "South Dakota", "North Carolina", "Michigan", "New Jersey", "Indiana", "Florida", "Nevada", "Iowa", "Rhode Island", "Maine", "Massachusetts", "Kentucky", "New Mexico", "Alabama", "Washington", "West Virginia", "Colorado", "Maryland", "Connecticut", "Minnesota", "Georgia", "California", "New Hampshire", "Wisconsin", "Oregon", "South Carolina"]

states.sort()

with open("us_states.txt", "w") as f:
    for state in states:
        f.write(state + "\n")


