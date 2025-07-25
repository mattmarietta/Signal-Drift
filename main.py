import data_simulator
import json


if __name__ == "__main__":
    
    # Create the generator and loop through it to print each event.
    for event in data_simulator.generate_message_stream():
        # Use json.dumps for the output to be formatted nicely
        print(json.dumps(event, indent=2))
        