#Import json and functions from the data_simulator and scoring_engine modules
from data_simulator import generate_message_stream, scripted_conversation
from scoring_engine import context_score_message, base_score_message
import json
import os

#Bonus: biometric module
from biometric import get_hrv

#Define global constants for window size and threshold
WINDOW_SIZE = 5
TRUST_DECAY_THRESHOLD = 0.5
LOG_FILE = "misalignment_log.json"

#Make a new function for appending to the log file
#Bonus function
def append_to_json(log_entry):
    #Check if the log file already exists and load its data
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    #Add the  flagged entry and write the whole list back to the file so we can keep all of the history
    logs.append(log_entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)
    print(f"\t[!] Trust decay event logged to {LOG_FILE}")



def run_drift_simulation():
    print("*** Starting Drift Simulation ***")

    #For each user we see in the conversation, keep track of their recent scores and last score
    #Dynamically initialize user states based on the scripted conversation, add more users to script if needed
    all_users = set(message["user"] for message in scripted_conversation)
    user_states = {user: {"recent_scores": [], "last_score": 0.0} for user in all_users}
    print(f"Successfully initialized states for users: {list(all_users)}\n")

    #Set user and message processing by iterating through the stream
    for message in generate_message_stream():
        user = message["user"]
        text = message["text"]
        
        #Retrieve the state for the current user
        user_state = user_states[user]

        #Get a base score in order to generate the HRV for the scoring to be applied    
        base_score, _ = base_score_message(text)
        synthetic_hrv = get_hrv(base_score)

        #Score the current message using the scoring engine
        #!! Keep in mind that the drift score is not compared to the threshold. Only average score is compared.
        drift_score, reason = context_score_message( current_text=text, last_score=user_state["last_score"], synthetic_hrv=synthetic_hrv)

        #Update the users sliding window of scores by appending and removing first score
        user_state["recent_scores"].append(drift_score)
        if len(user_state["recent_scores"]) > WINDOW_SIZE:
            user_state["recent_scores"].pop(0)

        
        #Make a log entry for the message with the drift score and reason
        log_entry = {
            "timestamp": message["timestamp"],
            "user": user,
            "message_text": text,
            "synthetic_hrv": synthetic_hrv,
            "analysis": {
                "drift_score": drift_score,
                "reason": reason
            },
            "trust_decay_analysis": {
                "triggered": False,
                "average_score_in_window": None
            }
        }
        
        #If the users window is full, check for the trust decay
        if len(user_state["recent_scores"]) == WINDOW_SIZE:
            average_score = sum(user_state["recent_scores"]) / WINDOW_SIZE
            log_entry["trust_decay_analysis"]["average_score_in_window"] = round(average_score, 2)
            
            #If the avg score over the window exceeds the threshold, we flag it
            if average_score > TRUST_DECAY_THRESHOLD:
                log_entry["trust_decay_analysis"]["triggered"] = True
                log_entry["trust_decay_analysis"]["warning_message"] = f"Potential trust decay in user {user} - intervention suggested!"

                #Log it to the file using the function
                append_to_json(log_entry)

        #Use json dumps to format the log for readability
        print(json.dumps(log_entry, indent=2))
        if log_entry["trust_decay_analysis"]["triggered"]:
            print(f"\n\t[!!!!]  [{log_entry['trust_decay_analysis']['warning_message']}\n")

        #Update user's last score for the next iterations context
        user_state["last_score"] = drift_score

    #End of simulation
    print("\n*** Simulation Complete ***")

if __name__ == "__main__":
    #Make sure log is clean before the run
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    run_drift_simulation()