#Import json and functions from the data_simulator and scoring_engine modules
from data_simulator import generate_message_stream, scripted_conversation
from scoring_engine import context_score_message
import json

#Define global constants for window size and threshold
WINDOW_SIZE = 5
TRUST_DECAY_THRESHOLD = 0.5

def run_drift_simulation():
    print("*** Starting Drift Simulation ***")

    #For each user we see in the conversation, keep track of their recent scores and last score
    all_users = set(message["user"] for message in scripted_conversation)
    user_states = {user: {"recent_scores": [], "last_score": 0.0} for user in all_users}
    print(f"Successfully initialized states for users: {list(all_users)}\n")

    #Set user and message processing by iterating through the stream
    for message in generate_message_stream():
        user = message["user"]
        text = message["text"]
        
        #Retrieve the state for the current user
        user_state = user_states[user]

        #Score the current message using the scoring engine
        #!! Keep in mind that the drift score is not compared to the threshold. Only average score is.
        drift_score, reason = context_score_message( current_text=text, last_score=user_state["last_score"])

        #Update the users sliding window of scores by appending and removing first score
        user_state["recent_scores"].append(drift_score)
        if len(user_state["recent_scores"]) > WINDOW_SIZE:
            user_state["recent_scores"].pop(0)

        
        #Make a log entry for the message with the drift score and reason
        log_entry = {
            "timestamp": message["timestamp"],
            "user": user,
            "message_text": text,
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
        
        #Use json dumps to format the log for readability
        print(json.dumps(log_entry, indent=2))
        if log_entry["trust_decay_analysis"]["triggered"]:
            print(f"\n\t[!!!!]  [{log_entry['trust_decay_analysis']['warning_message']}\n")

        #Update user's last score for the next iterations context
        user_state["last_score"] = drift_score

    #End of simulation
    print("\n*** Simulation Complete ***")

if __name__ == "__main__":
    run_drift_simulation()